"""
Customer analysis and segmentation module
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from .config import SAMPLING_CONFIG

class CustomerAnalysis:
    """Customer analysis and segmentation using K-means clustering"""
    
    def __init__(self, n_clusters=4):
        """
        Initialize the Customer Analysis model
        
        Parameters:
        -----------
        n_clusters : int, optional
            Number of clusters for customer segmentation, default is 4
        """
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = None
        self.data = None
        self.feature_cols = None
        self.clusters = None
        self.cluster_centers = None
        
    def prepare_data(self, data, feature_cols):
        """
        Prepare data for customer segmentation
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The dataset containing customer information
        feature_cols : list
            List of column names to use as features for segmentation
            
        Returns:
        --------
        pandas.DataFrame
            The prepared data
        """
        # Store the data and column names for later use
        self.data = data.copy()
        self.feature_cols = feature_cols
        
        # Check that all feature columns exist in the data
        missing_cols = [col for col in feature_cols if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in the data")
        
        # Handle missing values - use simple imputation for now
        for col in feature_cols:
            self.data[col] = self.data[col].fillna(self.data[col].mean())
        
        return self.data
    
    def fit(self, data, feature_cols):
        """
        Fit the customer segmentation model to the data
        
        Parameters:
        -----------
        data : pandas.DataFrame
            The dataset containing customer information
        feature_cols : list
            List of column names to use as features for segmentation
            
        Returns:
        --------
        self
            The fitted model object
        """
        # Prepare data
        self.prepare_data(data, feature_cols)
        
        # Extract features for clustering
        features = self.data[self.feature_cols].values
        
        # Standardize the features
        self.scaler = StandardScaler()
        scaled_features = self.scaler.fit_transform(features)
        
        # Apply KMeans clustering
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        cluster_labels = self.model.fit_predict(scaled_features)
        
        # Store cluster assignments and centers
        self.clusters = cluster_labels
        self.cluster_centers = self.model.cluster_centers_
        
        # Add cluster labels to data
        self.data['cluster'] = cluster_labels
        
        return self
    
    def get_cluster_profiles(self):
        """
        Get profile information for each cluster
        
        Returns:
        --------
        pandas.DataFrame
            DataFrame with cluster profiles
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
        
        # Calculate aggregate statistics for each cluster
        profiles = self.data.groupby('cluster').agg({
            **{col: ['mean', 'std', 'min', 'max'] for col in self.feature_cols},
            'cluster': 'size'
        })
        
        # Rename the size column to count
        profiles.columns = profiles.columns.map(lambda x: f'{x[0]}_{x[1]}' if x[0] != 'cluster' else 'count')
        
        # Calculate percentage of total
        profiles['percentage'] = profiles['count'] / profiles['count'].sum() * 100
        
        # Rename clusters to more meaningful names based on characteristics
        # This is a simple approach - in a real-world scenario, we'd use more
        # sophisticated logic to name clusters
        
        # First, identify key characteristics of each cluster
        characteristics = {}
        
        for cluster in range(self.n_clusters):
            cluster_data = profiles.loc[cluster]
            key_features = {}
            
            # For each feature, determine if it's high, medium, or low
            # compared to other clusters
            for feature in self.feature_cols:
                mean_col = f"{feature}_mean"
                feature_values = profiles[mean_col].values
                cluster_value = cluster_data[mean_col]
                
                # Simple percentile-based classification
                if cluster_value <= np.percentile(feature_values, 25):
                    key_features[feature] = "Low"
                elif cluster_value >= np.percentile(feature_values, 75):
                    key_features[feature] = "High"
                else:
                    key_features[feature] = "Medium"
            
            characteristics[cluster] = key_features
        
        # Create cluster names based on key characteristics
        cluster_names = {}
        for cluster, features in characteristics.items():
            high_features = [f for f, v in features.items() if v == "High"]
            low_features = [f for f, v in features.items() if v == "Low"]
            
            if len(high_features) > 0:
                name = "High " + " & ".join(high_features[:2])
            elif len(low_features) > 0:
                name = "Low " + " & ".join(low_features[:2])
            else:
                name = "Average Customers"
                
            cluster_names[cluster] = name
        
        # Add names to profiles
        profiles['name'] = pd.Series(cluster_names)
        
        return profiles
    
    def get_customer_segments(self):
        """
        Get customer segments with cluster assignments
        
        Returns:
        --------
        pandas.DataFrame
            DataFrame with customer segments
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
        
        # Get cluster profiles to get the names
        profiles = self.get_cluster_profiles()
        
        # Create a mapping from cluster number to name
        cluster_to_name = profiles['name'].to_dict()
        
        # Create a copy of the original data with cluster and segment name
        segments = self.data.copy()
        segments['segment'] = segments['cluster'].map(cluster_to_name)
        
        return segments
    
    def plot_clusters(self, feature_x, feature_y):
        """
        Create a scatter plot of clusters for two selected features
        
        Parameters:
        -----------
        feature_x : str
            Column name for the x-axis
        feature_y : str
            Column name for the y-axis
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
        
        if feature_x not in self.feature_cols or feature_y not in self.feature_cols:
            raise ValueError(f"Features must be one of {self.feature_cols}")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get customer segments with names
        segments = self.get_customer_segments()
        
        # Get unique segments and assign different colors
        unique_segments = segments['segment'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_segments)))
        
        # Plot each segment
        for i, segment in enumerate(unique_segments):
            mask = segments['segment'] == segment
            ax.scatter(
                segments.loc[mask, feature_x],
                segments.loc[mask, feature_y],
                c=[colors[i]],
                label=segment,
                alpha=0.7,
                s=50
            )
        
        # Plot cluster centers
        x_idx = self.feature_cols.index(feature_x)
        y_idx = self.feature_cols.index(feature_y)
        
        # Transform cluster centers back to original scale
        centers_original = self.scaler.inverse_transform(self.cluster_centers)
        
        ax.scatter(
            centers_original[:, x_idx],
            centers_original[:, y_idx],
            c='black',
            marker='X',
            s=100,
            label='Cluster Centers'
        )
        
        # Labels and title
        ax.set_xlabel(feature_x)
        ax.set_ylabel(feature_y)
        ax.set_title('Customer Segmentation')
        ax.legend()
        
        return fig
    
    def plot_feature_importance(self):
        """
        Create a heatmap showing feature importance for each cluster
        
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
        
        # Get cluster profiles
        profiles = self.get_cluster_profiles()
        
        # Create a DataFrame with mean values for each feature by cluster
        mean_cols = [f"{feature}_mean" for feature in self.feature_cols]
        feature_importance = profiles[mean_cols].copy()
        
        # Rename columns to original feature names
        feature_importance.columns = [col.replace('_mean', '') for col in feature_importance.columns]
        
        # Get cluster names
        cluster_names = profiles['name'].tolist()
        feature_importance.index = cluster_names
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create heatmap
        sns.heatmap(
            feature_importance, 
            annot=True, 
            cmap='YlGnBu', 
            fmt='.2f',
            ax=ax
        )
        
        ax.set_title('Feature Importance by Customer Segment')
        
        return fig