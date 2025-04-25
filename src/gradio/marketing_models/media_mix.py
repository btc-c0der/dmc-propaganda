"""
Media Mix Modeling module using PyMC Marketing
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import warnings
import scipy.optimize as optimize
from pymc_marketing.mmm import MMM

from .config import DEFAULT_PRIORS, SAMPLING_CONFIG

warnings.filterwarnings("ignore")

class MediaMixModel:
    """Media Mix Modeling using PyMC Marketing"""
    
    def __init__(self, priors=None):
        """
        Initialize the Media Mix Model with configurable priors
        
        Parameters:
        -----------
        priors : dict, optional
            Dictionary of prior values for the model
        """
        self.priors = priors or DEFAULT_PRIORS['mmm']
        self.model = None
        self.trace = None
        self.summary = None
        
    def prepare_data(self, data, channels, target):
        """
        Prepare data for media mix modeling
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The dataset containing marketing channel and target variables
        channels : list
            List of column names for marketing channels
        target : str
            Column name for the target variable (e.g., sales)
            
        Returns:
        --------
        tuple
            X (features matrix), y (target vector)
        """
        # Store the data and column names for later use
        self.data = data.copy()
        self.channels = channels
        self.target = target
        
        # Extract features and target
        X = np.array(data[channels])
        y = np.array(data[target])
        
        return X, y
    
    def build_model(self, X, y):
        """
        Build the PyMC Marketing media mix model
        
        Parameters:
        -----------
        X : numpy.ndarray
            Feature matrix with marketing channel data
        y : numpy.ndarray
            Target variable (sales, conversions, etc.)
        """
        # Create the model using PyMC Marketing's MMM class
        with pm.Model() as self.model:
            # Create an MMM instance instead of MMMModelBuilder
            mmm = MMM()
            
            # Add media channels
            for i, channel in enumerate(self.channels):
                # Add each channel's data to the model
                mmm.add_media(
                    name=channel,
                    media_data=X[:, i],
                    adstock=None,  # Use default adstock
                    saturation=None  # Use default saturation
                )
            
            # Add the response variable
            mmm.add_response(y)
            
            # Build the model
            mmm.build()
            
            # Set priors for model parameters
            # Note: The PyMC Marketing's MMM class handles priors internally,
            # so we don't need to set them manually here

    def fit(self, data, channels, target):
        """
        Fit the media mix model to data
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The dataset containing marketing channel and target variables
        channels : list
            List of column names for marketing channels
        target : str
            Column name for the target variable (e.g., sales)
            
        Returns:
        --------
        self
            The fitted model object
        """
        # Prepare data
        X, y = self.prepare_data(data, channels, target)
        
        # Build the model
        self.build_model(X, y)
        
        # Sample from the model
        with self.model:
            self.trace = pm.sample(
                draws=SAMPLING_CONFIG['draws'],
                tune=SAMPLING_CONFIG['tune'],
                chains=SAMPLING_CONFIG['chains'],
                target_accept=SAMPLING_CONFIG['target_accept'],
                return_inferencedata=SAMPLING_CONFIG['return_inferencedata']
            )
        
        # Generate summary statistics
        self.summary = az.summary(self.trace)
        
        return self
    
    def predict(self, data=None):
        """
        Generate predictions from the fitted model
        
        Parameters:
        -----------
        data : pandas.DataFrame, optional
            New data to predict on. If None, use the training data.
            
        Returns:
        --------
        numpy.ndarray
            Array of predictions
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        # Use training data if no new data is provided
        if data is None:
            data = self.data
            X = np.array(data[self.channels])
        else:
            # Extract features from the new data
            X = np.array(data[self.channels])
        
        # Extract parameters from trace
        alpha_samples = self.trace.posterior['alpha'].values.flatten()
        beta_samples = self.trace.posterior['beta'].values
        
        # Reshape beta to work with matrix multiplication
        beta_samples = np.mean(beta_samples, axis=0)  # Average over chains
        
        # Calculate predictions
        n_samples = len(alpha_samples)
        n_datapoints = X.shape[0]
        predictions = np.zeros((n_samples, n_datapoints))
        
        for i in range(n_samples):
            alpha = alpha_samples[i]
            beta = beta_samples[i]
            
            # Linear component: alpha + X * beta
            predictions[i] = alpha + np.dot(X, beta)
            
        # Return mean prediction across all samples
        return predictions.mean(axis=0)
    
    def get_roi_estimates(self):
        """
        Calculate ROI for each marketing channel
        
        Returns:
        --------
        pandas.DataFrame
            DataFrame with ROI estimates and confidence intervals
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        # Extract beta parameters from trace
        beta_samples = self.trace.posterior['beta'].values
        
        # Calculate mean spend for each channel
        mean_spend = self.data[self.channels].mean().values
        
        # Calculate ROI for each sample
        n_samples = beta_samples.shape[1]
        n_channels = len(self.channels)
        roi_samples = np.zeros((n_samples, n_channels))
        
        # Calculate ROI as beta / mean_spend for each channel
        for i in range(n_channels):
            # Extract beta samples for this channel
            channel_beta = beta_samples[:, :, i].flatten()
            
            # Calculate ROI: Impact per $ spent
            roi_samples[:, i] = channel_beta / mean_spend[i]
            
        # Calculate mean and CI for ROI
        roi_mean = np.mean(roi_samples, axis=0)
        roi_lower = np.percentile(roi_samples, 2.5, axis=0)
        roi_upper = np.percentile(roi_samples, 97.5, axis=0)
        
        # Create DataFrame with results
        roi_df = pd.DataFrame({
            'Channel': self.channels,
            'ROI': roi_mean,
            'Lower_CI': roi_lower,
            'Upper_CI': roi_upper
        })
        
        # Sort by ROI in descending order
        roi_df = roi_df.sort_values('ROI', ascending=False)
        
        return roi_df
    
    def plot_channel_contributions(self, save_path=None):
        """
        Plot the contribution of each marketing channel
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the plot to
            
        Returns:
        --------
        matplotlib.figure.Figure
            The generated figure
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        # Extract beta parameters from trace
        beta_samples = self.trace.posterior['beta'].values
        
        # Calculate mean beta for each channel
        beta_mean = np.mean(beta_samples, axis=(0, 1))
        
        # Calculate contribution as beta * mean_spend
        mean_spend = self.data[self.channels].mean().values
        contributions = beta_mean * mean_spend
        
        # Calculate contribution percentages
        total_contribution = np.sum(contributions)
        contribution_pct = contributions / total_contribution * 100
        
        # Sort channels by contribution
        sorted_indices = np.argsort(contribution_pct)[::-1]
        sorted_channels = [self.channels[i] for i in sorted_indices]
        sorted_contributions = contribution_pct[sorted_indices]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar plot
        bars = ax.bar(
            sorted_channels,
            sorted_contributions,
            color=plt.cm.viridis(np.linspace(0, 0.8, len(sorted_channels)))
        )
        
        # Add labels and formatting
        ax.set_title('Marketing Channel Contributions', fontsize=15)
        ax.set_xlabel('Channel', fontsize=12)
        ax.set_ylabel('Contribution (%)', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add percentage labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f'{height:.1f}%',
                ha='center',
                fontsize=10
            )
            
        plt.tight_layout()
        
        # Save if path is provided
        if save_path:
            plt.savefig(save_path)
            
        return fig
    
    def optimize_budget(self, total_budget, min_budget=None, max_budget=None):
        """
        Optimize marketing budget allocation
        
        Parameters:
        -----------
        total_budget : float
            Total budget to allocate
        min_budget : dict, optional
            Minimum budget for each channel
        max_budget : dict, optional
            Maximum budget for each channel
            
        Returns:
        --------
        dict
            Optimal budget allocation for each channel
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        # Extract mean beta for each channel
        beta_samples = self.trace.posterior['beta'].values
        beta_mean = np.mean(beta_samples, axis=(0, 1))
        
        # Set up budget constraints
        n_channels = len(self.channels)
        
        # Default min and max budgets if not provided
        if min_budget is None:
            min_budget = {channel: 0 for channel in self.channels}
        
        if max_budget is None:
            max_budget = {channel: total_budget for channel in self.channels}
            
        # Initial guess: equal allocation
        x0 = np.ones(n_channels) * total_budget / n_channels
        
        # Budget constraint functions
        def constraint_sum(x):
            return np.sum(x) - total_budget
        
        constraints = [{'type': 'eq', 'fun': constraint_sum}]
        
        # Bounds for each channel
        bounds = [(min_budget[self.channels[i]], max_budget[self.channels[i]]) 
                  for i in range(n_channels)]
        
        # Objective function to maximize (negative for minimization)
        def objective(x):
            return -np.sum(beta_mean * x)
        
        # Run optimization
        result = optimize.minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Create dictionary with optimal allocation
        optimal = {self.channels[i]: result.x[i] for i in range(n_channels)}
        
        return optimal
    
    def plot_budget_optimization(self, total_budget, save_path=None):
        """
        Plot current vs. optimal budget allocation
        
        Parameters:
        -----------
        total_budget : float
            Total budget to allocate
        save_path : str, optional
            Path to save the plot to
            
        Returns:
        --------
        matplotlib.figure.Figure
            The generated figure
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        # Calculate current allocation
        current_spend = self.data[self.channels].mean().values
        current_total = np.sum(current_spend)
        current_allocation = {
            self.channels[i]: current_spend[i] / current_total * total_budget
            for i in range(len(self.channels))
        }
        
        # Get optimal allocation
        optimal_allocation = self.optimize_budget(total_budget)
        
        # Prepare data for plotting
        channels = self.channels
        current_values = [current_allocation[c] for c in channels]
        optimal_values = [optimal_allocation[c] for c in channels]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(channels))
        width = 0.35
        
        # Create grouped bar plot
        ax.bar(x - width/2, current_values, width, label='Current', color='skyblue')
        ax.bar(x + width/2, optimal_values, width, label='Optimal', color='orange')
        
        # Add labels and formatting
        ax.set_title('Current vs. Optimal Budget Allocation', fontsize=15)
        ax.set_xlabel('Channel', fontsize=12)
        ax.set_ylabel('Budget ($)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(channels, rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.legend()
        
        # Add budget labels on top of bars
        for i, v in enumerate(current_values):
            ax.text(
                i - width/2, 
                v + 0.01 * total_budget,
                f'${v:.0f}',
                ha='center',
                fontsize=9
            )
            
        for i, v in enumerate(optimal_values):
            ax.text(
                i + width/2, 
                v + 0.01 * total_budget,
                f'${v:.0f}',
                ha='center',
                fontsize=9
            )
            
        plt.tight_layout()
        
        # Save if path is provided
        if save_path:
            plt.savefig(save_path)
            
        return fig