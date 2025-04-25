"""
Unit tests for Media Mix Modeling module
"""
import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from marketing_models.media_mix import MediaMixModel
from marketing_models.config import DEFAULT_PRIORS, SAMPLING_CONFIG

class TestMediaMixModel:
    """Tests for the MediaMixModel class"""
    
    def test_init(self):
        """Test initialization with default and custom priors"""
        # Test with default priors
        model = MediaMixModel()
        assert model.priors == DEFAULT_PRIORS['mmm']
        
        # Test with custom priors
        custom_priors = {
            'alpha_prior_mean': 0.5,
            'alpha_prior_sd': 0.5,
            'beta_prior_mean': 0.5,
            'beta_prior_sd': 0.5
        }
        model = MediaMixModel(priors=custom_priors)
        assert model.priors == custom_priors
    
    def test_prepare_data(self, sample_mmm_data):
        """Test data preparation"""
        model = MediaMixModel()
        channels = ['tv', 'radio', 'social', 'search', 'email']
        target = 'sales'
        
        X, y = model.prepare_data(sample_mmm_data, channels, target)
        
        # Check dimensions
        assert X.shape == (len(sample_mmm_data), len(channels))
        assert y.shape == (len(sample_mmm_data),)
        
        # Check that channels and target are stored
        assert model.channels == channels
        assert model.target == target
        
        # Check that the data matches the input
        for i, channel in enumerate(channels):
            assert np.array_equal(X[:, i], sample_mmm_data[channel].values)
        assert np.array_equal(y, sample_mmm_data[target].values)
    
    @pytest.mark.slow
    def test_fit_model(self, sample_mmm_data, monkeypatch):
        """Test model fitting (mocked for speed)"""
        model = MediaMixModel()
        
        # Mock the MMMModelBuilder to avoid actual model building and fitting
        class MockMMM:
            def __init__(self):
                pass
                
            def add_media(self, name, media_data, adstock=None, saturation=None):
                pass
                
            def add_response(self, response_data):
                pass
                
            def build(self):
                pass
        
        # Mock the sampling to make test run faster
        def mock_sample(*args, **kwargs):
            import arviz as az
            # Create a minimal mock trace
            dims = {"chain": 2, "draw": 10, "channel": ['tv', 'radio', 'social', 'search', 'email']}
            coords = {"channel": ['tv', 'radio', 'social', 'search', 'email']}
            
            # Create mock data for posterior
            mock_posterior = {
                "alpha": np.random.normal(1, 0.1, size=(2, 10)),
                "beta": np.random.normal(0.5, 0.1, size=(2, 10, 5)),
                "sigma": np.random.normal(0.2, 0.05, size=(2, 10))
            }
            
            return az.from_dict(posterior=mock_posterior, dims=dims, coords=coords)
        
        # Apply the mocks
        import pymc as pm
        from pymc_marketing.mmm import MMM
        monkeypatch.setattr(model, "build_model", lambda X, y: setattr(model, "model", pm.Model()))
        monkeypatch.setattr(pm, "sample", mock_sample)
        
        # Now test fitting
        channels = ['tv', 'radio', 'social', 'search', 'email']
        target = 'sales'
        model.fit(sample_mmm_data, channels, target)
        
        # Check that the model was built and trace is available
        assert model.model is not None
        assert model.trace is not None
        assert model.summary is not None
        
    def test_roi_estimates(self, monkeypatch):
        """Test ROI estimation logic"""
        model = MediaMixModel()
        model.channels = ['tv', 'radio', 'social']
        model.data = pd.DataFrame({
            'tv': [1000, 2000, 3000],
            'radio': [500, 600, 700],
            'social': [300, 400, 500]
        })
        
        # Mock the model so we can test get_roi_estimates
        model.model = "dummy_model"
        
        # Mock the trace
        import arviz as az
        
        # Create a mock trace with predictable values
        dims = {"chain": 1, "draw": 10, "channel": model.channels}
        coords = {"channel": model.channels}
        
        mock_beta = np.array([[[0.5, 0.3, 0.7]]])  # Simple fixed betas for predictable results
        mock_beta = np.repeat(mock_beta, 10, axis=1)  # Repeat for 10 draws
        
        mock_posterior = {
            "beta": mock_beta
        }
        
        model.trace = az.from_dict(posterior=mock_posterior, dims=dims, coords=coords)
        
        # Run ROI estimation
        roi_df = model.get_roi_estimates()
        
        # Check that ROIs were calculated correctly
        assert len(roi_df) == 3  # One row per channel
        assert all(col in roi_df.columns for col in ['Channel', 'ROI', 'Lower_CI', 'Upper_CI'])
        
        # Check that the ROI values are as expected
        # Given beta=[0.5, 0.3, 0.7] and mean_spend=[2000, 600, 400]
        # Expected ROI = beta / mean_spend
        expected_roi = {
            'tv': 0.5 / 2000,
            'radio': 0.3 / 600,
            'social': 0.7 / 400
        }
        
        for index, row in roi_df.iterrows():
            channel = row['Channel']
            assert np.isclose(row['ROI'], expected_roi[channel], rtol=1e-5)
    
    def test_plot_channel_contributions(self, monkeypatch):
        """Test channel contribution plotting"""
        model = MediaMixModel()
        model.channels = ['tv', 'radio', 'social', 'search', 'email']
        model.model = "dummy_model"
        
        # Mock the trace
        import arviz as az
        
        # Create a mock trace with predictable values
        dims = {"chain": 1, "draw": 10, "channel": model.channels}
        coords = {"channel": model.channels}
        
        mock_beta = np.array([[[0.5, 0.3, 0.7, 0.2, 0.1]]])  # Simple fixed betas
        mock_beta = np.repeat(mock_beta, 10, axis=1)  # Repeat for 10 draws
        
        mock_posterior = {
            "beta": mock_beta
        }
        
        model.trace = az.from_dict(posterior=mock_posterior, dims=dims, coords=coords)
        
        # Run the plotting function
        fig = model.plot_channel_contributions()
        
        # Basic checks on the figure
        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1  # Should have one axis
        
        # Clean up
        plt.close(fig)
    
    def test_optimize_budget(self, monkeypatch):
        """Test budget optimization logic"""
        model = MediaMixModel()
        model.channels = ['tv', 'radio', 'social']
        model.model = "dummy_model"
        
        # Mock the trace
        import arviz as az
        
        # Create a mock trace with predictable values
        dims = {"chain": 1, "draw": 10, "channel": model.channels}
        coords = {"channel": model.channels}
        
        mock_beta = np.array([[[0.5, 0.3, 0.7]]])  # Simple fixed betas
        mock_beta = np.repeat(mock_beta, 10, axis=1)  # Repeat for 10 draws
        
        mock_posterior = {
            "beta": mock_beta
        }
        
        model.trace = az.from_dict(posterior=mock_posterior, dims=dims, coords=coords)
        
        # Run budget optimization
        total_budget = 10000
        optimal = model.optimize_budget(total_budget)
        
        # Check that optimization produced a valid result
        assert isinstance(optimal, dict)
        assert all(channel in optimal for channel in model.channels)
        
        # Check that we used the entire budget
        assert np.isclose(sum(optimal.values()), total_budget, rtol=1e-5)
        
        # Check that channels with higher betas get more budget
        # In our mock, social has the highest beta, followed by tv, then radio
        assert optimal['social'] > optimal['tv'] > optimal['radio']