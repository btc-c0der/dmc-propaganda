"""
Configuration settings for PyMC Marketing models
"""

# Default priors configuration
DEFAULT_PRIORS = {
    'mmm': {  # Media Mix Modeling
        'alpha': 0.1,  # Intercept prior
        'beta': 0.5,   # Channel effect prior
        'sigma': 0.2,  # Error term prior
        'gamma': 0.7,  # Adstock/carryover prior
        'seasonality_prior_scale': 0.1
    },
    'clv': {  # Customer Lifetime Value
        'r_prior_alpha': 1.0,
        'r_prior_beta': 1.0,
        'alpha_prior_alpha': 1.0,
        'alpha_prior_beta': 1.0
    },
    'attribution': {  # Attribution models
        'shape_prior': 0.5,
        'scale_prior': 1.0
    }
}

# MCMC sampling configuration
SAMPLING_CONFIG = {
    'draws': 1000,
    'tune': 1000,
    'chains': 2,
    'target_accept': 0.8,
    'return_inferencedata': True
}

# Model evaluation metrics to track
EVALUATION_METRICS = [
    'mae',      # Mean Absolute Error
    'rmse',     # Root Mean Squared Error
    'mape',     # Mean Absolute Percentage Error
    'r_squared' # R-squared
]

# Feature transformation settings
TRANSFORMATIONS = {
    'adstock': {
        'max_lag': 8,
        'normalize': True
    },
    'diminishing_returns': {
        'method': 'hill',  # Options: 'hill', 'logistic', 'power'
        'normalize': True
    },
    'seasonality': {
        'yearly': True,
        'weekly': True,
        'fourier_order': 5
    }
}