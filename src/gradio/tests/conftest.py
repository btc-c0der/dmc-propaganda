"""
Test configuration and fixtures for Gradio app tests
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_mmm_data():
    """Generate sample data for media mix modeling tests"""
    np.random.seed(123)
    dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
    data = pd.DataFrame({
        'date': dates,
        'tv': np.random.gamma(5, 1000, size=30),
        'radio': np.random.gamma(2, 800, size=30),
        'social': np.random.gamma(10, 500, size=30),
        'search': np.random.gamma(8, 300, size=30),
        'email': np.random.gamma(3, 200, size=30)
    })
    
    # Create synthetic response
    data['sales'] = 100000 + 0.5*data['tv'] + 0.3*data['radio'] + 0.7*data['social'] + 0.9*data['search'] + 0.2*data['email'] + np.random.normal(0, 5000, size=30)
    
    return data

@pytest.fixture
def sample_clv_data():
    """Generate sample data for CLV modeling tests"""
    np.random.seed(456)
    n_customers = 100
    
    # Generate frequency, recency, T
    frequency = np.random.poisson(3, size=n_customers)
    T = 30 + np.random.gamma(2, 10, size=n_customers)
    recency = np.array([np.random.uniform(0, t) if f > 0 else 0 
                      for f, t in zip(frequency, T)])
    
    # Generate monetary values
    monetary = 10 + np.random.gamma(5, 20, size=n_customers)
    
    # Create DataFrame
    data = pd.DataFrame({
        'customer_id': [f'C{i:04d}' for i in range(n_customers)],
        'frequency': frequency,
        'recency': recency,
        'T': T,
        'monetary_value': monetary
    })
    
    return data

@pytest.fixture
def mock_api_responses():
    """Mock API responses for testing API integration"""
    return {
        'login': {
            'success': {
                'token': 'test-token-123',
                'user': {'name': 'Test User', 'email': 'test@example.com'}
            },
            'failure': {'message': 'Invalid credentials'}
        },
        'clients': {
            'success': [
                {'id': '1', 'name': 'Client A', 'industry': 'Technology'},
                {'id': '2', 'name': 'Client B', 'industry': 'Healthcare'}
            ],
            'failure': {'message': 'Unauthorized access'}
        },
        'campaigns': {
            'success': [
                {'id': '101', 'name': 'Campaign 1', 'client_id': '1', 'status': 'active'},
                {'id': '102', 'name': 'Campaign 2', 'client_id': '1', 'status': 'completed'}
            ],
            'failure': {'message': 'Unauthorized access'}
        },
        'analytics': {
            'success': [
                {'campaign_id': '101', 'impressions': 10000, 'clicks': 500, 'conversions': 50},
                {'campaign_id': '102', 'impressions': 8000, 'clicks': 400, 'conversions': 40}
            ],
            'failure': {'message': 'Unauthorized access'}
        }
    }