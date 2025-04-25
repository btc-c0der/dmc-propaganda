"""
Gradio interface for PyMC Marketing models
"""
import os
import pandas as pd
import numpy as np
import gradio as gr
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
import json
import base64
from io import BytesIO

from .media_mix import MediaMixModel
from .clv import CustomerLifetimeValue
from .customer import CustomerAnalysis

# Sample data generation functions for demo purposes
def generate_sample_mmm_data():
    """Generate sample data for media mix modeling"""
    np.random.seed(123)
    dates = pd.date_range(start='2023-01-01', periods=90, freq='D')
    data = pd.DataFrame({
        'date': dates,
        'tv': np.random.gamma(5, 1000, size=90),
        'radio': np.random.gamma(2, 800, size=90),
        'social': np.random.gamma(10, 500, size=90),
        'search': np.random.gamma(8, 300, size=90),
        'email': np.random.gamma(3, 200, size=90)
    })
    
    # Create synthetic response with realistic effects
    tv_effect = 0.5 * data['tv']
    radio_effect = 0.3 * data['radio']
    social_effect = 0.7 * data['social']
    search_effect = 0.9 * data['search']
    email_effect = 0.2 * data['email']
    
    # Add weekly seasonality
    weekday_effect = 20000 * np.sin(2 * np.pi * dates.dayofweek / 7)
    
    # Add random noise
    noise = np.random.normal(0, 5000, size=90)
    
    # Combine all effects
    data['sales'] = 100000 + tv_effect + radio_effect + social_effect + search_effect + email_effect + weekday_effect + noise
    data['sales'] = data['sales'].clip(lower=0)  # No negative sales
    
    return data

def generate_sample_clv_data():
    """Generate sample data for CLV modeling"""
    np.random.seed(456)
    n_customers = 500
    
    # Generate frequency, recency, T
    frequency = np.random.poisson(3, size=n_customers)
    T = 30 + np.random.gamma(2, 10, size=n_customers)  # Time since first purchase (days)
    
    # Recency must be less than T
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

def generate_sample_customer_data():
    """Generate sample data for customer segmentation"""
    np.random.seed(789)
    n_customers = 500
    
    # Generate demographic and behavioral features
    age = np.random.normal(40, 10, size=n_customers).clip(18, 75)
    income = np.random.gamma(10, 5000, size=n_customers)
    tenure = np.random.gamma(2, 2, size=n_customers).clip(0, 15)  # Years as customer
    purchases = np.random.poisson(5, size=n_customers)
    avg_order_value = np.random.gamma(5, 20, size=n_customers)
    website_visits = np.random.poisson(20, size=n_customers)
    
    # Add correlations
    income = income + 100 * age + np.random.normal(0, 10000, size=n_customers)
    avg_order_value = avg_order_value + 0.001 * income + np.random.normal(0, 10, size=n_customers)
    website_visits = website_visits + purchases * 2 + np.random.poisson(5, size=n_customers)
    
    # Create DataFrame
    data = pd.DataFrame({
        'customer_id': [f'C{i:04d}' for i in range(n_customers)],
        'age': age.astype(int),
        'income': income.clip(20000, 250000),
        'tenure': tenure,
        'purchases_last_year': purchases,
        'avg_order_value': avg_order_value,
        'website_visits_last_month': website_visits
    })
    
    return data

# Gradio interfaces
def create_mmm_interface():
    """Create Gradio interface for Media Mix Modeling"""
    
    def load_data(file):
        """Load data from uploaded file"""
        if file is None:
            return "No file uploaded. Using sample data.", generate_sample_mmm_data()
            
        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file.name)
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file.name)
            else:
                return "Unsupported file format. Please upload CSV or Excel file.", None
                
            # Validate essential columns
            required_columns = ["date"]  # Add required columns for MMM
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                return f"Error: Missing required columns: {', '.join(missing_columns)}", None
                
            return f"Successfully loaded data with {data.shape[0]} rows and {data.shape[1]} columns.", data
        except Exception as e:
            return f"Error loading file: {str(e)}", None
    
    def run_mmm(data_csv, target_col, date_col, channel_cols_str):
        """Run media mix modeling analysis"""
        try:
            # Parse inputs
            if data_csv is None:
                return "No data available. Please upload a file or use sample data.", None, None, None
                
            # Validate column names
            try:
                # Parse channel columns
                channel_cols = [col.strip() for col in channel_cols_str.split(',')]
                
                # Check if target column exists
                if target_col not in data_csv.columns:
                    return f"Error: Target column '{target_col}' not found in data.", None, None, None
                    
                # Check if date column exists
                if date_col not in data_csv.columns:
                    return f"Error: Date column '{date_col}' not found in data.", None, None, None
                    
                # Check if all channel columns exist
                missing_channels = [col for col in channel_cols if col not in data_csv.columns]
                if missing_channels:
                    return f"Error: Channel columns not found: {', '.join(missing_channels)}", None, None, None
            except Exception as e:
                return f"Error validating columns: {str(e)}", None, None, None
                
            # Initialize model
            mmm = MediaMixModel()
            
            # Fit model
            mmm.fit(data_csv, channels=channel_cols, target=target_col, date_col=date_col)
            
            # Generate ROI estimates
            roi_df = mmm.get_roi_estimates()
            roi_html = roi_df.to_html(index=False)
            
            # Generate plot
            fig = mmm.plot_channel_contributions()
            
            # Save plot to buffer
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            
            # Get budget optimization with even budget split
            total_budget = data_csv[channel_cols].sum().sum() / len(data_csv) * 30  # Monthly budget estimate
            optimal_budget = mmm.optimize_budget(total_budget)
            budget_html = pd.DataFrame({
                'Channel': list(optimal_budget.keys()),
                'Optimal Budget': list(optimal_budget.values())
            }).to_html(index=False)
            
            return "Media Mix Model successfully fitted!", roi_html, plot_base64, budget_html
            
        except Exception as e:
            return f"Error running model: {str(e)}", None, None, None
    
    with gr.Blocks() as mmm_interface:
        gr.Markdown("# Media Mix Modeling with PyMC Marketing")
        
        with gr.Row():
            with gr.Column():
                data_file = gr.File(label="Upload Data (CSV or Excel)")
                use_sample = gr.Button("Use Sample Data")
                data_info = gr.Textbox(label="Data Info", interactive=False)
                
                target_col = gr.Textbox(label="Target Column", value="sales")
                date_col = gr.Textbox(label="Date Column", value="date")
                channel_cols = gr.Textbox(label="Channel Columns (comma-separated)", value="tv,radio,social,search,email")
                run_button = gr.Button("Run Media Mix Model")
                
            with gr.Column():
                data_preview = gr.Dataframe(label="Data Preview")
        
        result = gr.Textbox(label="Result")
        loading_indicator = gr.HTML("""<div id="loading" style="display:none; text-align:center">
                                    <p>Calculating model - this may take a few moments...</p>
                                    <div class="loader"></div>
                                    </div>
                                    <style>
                                    .loader {
                                        border: 5px solid #f3f3f3;
                                        border-top: 5px solid #3498db;
                                        border-radius: 50%;
                                        width: 30px;
                                        height: 30px;
                                        animation: spin 2s linear infinite;
                                        margin: auto;
                                    }
                                    @keyframes spin {
                                        0% { transform: rotate(0deg); }
                                        100% { transform: rotate(360deg); }
                                    }
                                    </style>""")
        
        with gr.Accordion("Model Results", open=False):
            with gr.Tabs():
                with gr.TabItem("Channel Effects"):
                    # Using HTML to display the base64 image
                    channel_effects_plot = gr.HTML(label="Channel Effects")
                
                with gr.TabItem("ROI Estimates"):
                    roi_table = gr.HTML(label="ROI Estimates")
                
                with gr.TabItem("Budget Optimization"):
                    budget_table = gr.HTML(label="Optimal Budget Allocation")
        
        def load_and_preview_data(file):
            message, data = load_data(file)
            return message, data if data is not None else None
        
        def use_sample_data():
            data = generate_sample_mmm_data()
            return "Using sample data for Media Mix Modeling.", data
        
        data_file.upload(load_and_preview_data, inputs=[data_file], outputs=[data_info, data_preview])
        use_sample.click(use_sample_data, inputs=[], outputs=[data_info, data_preview])
        
        # Show loading indicator before running model
        def show_loading():
            return """<div id="loading" style="display:block; text-align:center">
                   <p>Calculating model - this may take a few moments...</p>
                   <div class="loader"></div>
                   </div>
                   <style>
                   .loader {
                       border: 5px solid #f3f3f3;
                       border-top: 5px solid #3498db;
                       border-radius: 50%;
                       width: 30px;
                       height: 30px;
                       animation: spin 2s linear infinite;
                       margin: auto;
                   }
                   @keyframes spin {
                       0% { transform: rotate(0deg); }
                       100% { transform: rotate(360deg); }
                   }
                   </style>"""
        
        def hide_loading():
            return """<div id="loading" style="display:none"></div>"""
        
        run_button.click(
            show_loading, 
            inputs=None, 
            outputs=loading_indicator,
            queue=False
        ).then(
            run_mmm, 
            inputs=[data_preview, target_col, date_col, channel_cols], 
            outputs=[result, roi_table, channel_effects_plot, budget_table]
        ).then(
            hide_loading,
            inputs=None,
            outputs=loading_indicator,
            queue=False
        )
    
    return mmm_interface

def create_clv_interface():
    """Create Gradio interface for Customer Lifetime Value modeling"""
    
    def load_data(file):
        """Load data from uploaded file"""
        if file is None:
            return "No file uploaded. Using sample data.", generate_sample_clv_data()
            
        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file.name)
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file.name)
            else:
                return "Unsupported file format. Please upload CSV or Excel file.", None
                
            return f"Successfully loaded data with {data.shape[0]} rows and {data.shape[1]} columns.", data
        except Exception as e:
            return f"Error loading file: {str(e)}", None
    
    def run_clv(data_csv, freq_col, recency_col, t_col, monetary_col):
        """Run CLV analysis"""
        try:
            # Parse inputs
            if data_csv is None:
                return "No data available. Please upload a file or use sample data.", None, None
                
            # Initialize model
            clv = CustomerLifetimeValue()
            
            # Fit model
            clv.fit(
                data=data_csv, 
                frequency_col=freq_col, 
                recency_col=recency_col, 
                T_col=t_col, 
                monetary_col=monetary_col
            )
            
            # Get customer segments
            segments_df = clv.segment_customers()
            
            # Create segment distribution DataFrame
            segment_counts = segments_df['segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            segment_counts['Percentage'] = segment_counts['Count'] / segment_counts['Count'].sum() * 100
            segments_html = segment_counts.to_html(index=False)
            
            # Generate plot
            fig = clv.plot_segments()
            
            # Save plot to buffer
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            
            return "CLV Model successfully fitted!", segments_html, plot_base64
            
        except Exception as e:
            return f"Error running model: {str(e)}", None, None
    
    with gr.Blocks() as clv_interface:
        gr.Markdown("# Customer Lifetime Value Modeling with PyMC Marketing")
        
        with gr.Row():
            with gr.Column():
                data_file = gr.File(label="Upload Data (CSV or Excel)")
                use_sample = gr.Button("Use Sample Data")
                data_info = gr.Textbox(label="Data Info", interactive=False)
                
                freq_col = gr.Textbox(label="Frequency Column", value="frequency")
                recency_col = gr.Textbox(label="Recency Column", value="recency")
                t_col = gr.Textbox(label="T Column (time since first purchase)", value="T")
                monetary_col = gr.Textbox(label="Monetary Value Column (optional)", value="monetary_value")
                run_button = gr.Button("Run CLV Model")
                
            with gr.Column():
                data_preview = gr.Dataframe(label="Data Preview")
        
        result = gr.Textbox(label="Result")
        
        with gr.Accordion("Model Results", open=False):
            with gr.Tabs():
                with gr.TabItem("Customer Segments"):
                    segment_table = gr.HTML(label="Segment Distribution")
                
                with gr.TabItem("Segment Plot"):
                    segment_plot = gr.HTML(label="Customer Segments")
        
        def load_and_preview_data(file):
            message, data = load_data(file)
            return message, data if data is not None else None
        
        def use_sample_data():
            data = generate_sample_clv_data()
            return "Using sample data for CLV Modeling.", data
        
        data_file.upload(load_and_preview_data, inputs=[data_file], outputs=[data_info, data_preview])
        use_sample.click(use_sample_data, inputs=[], outputs=[data_info, data_preview])
        
        run_button.click(
            run_clv, 
            inputs=[data_preview, freq_col, recency_col, t_col, monetary_col], 
            outputs=[result, segment_table, segment_plot]
        )
    
    return clv_interface

def create_customer_interface():
    """Create Gradio interface for Customer Analysis and Segmentation"""
    
    def load_data(file):
        """Load data from uploaded file"""
        if file is None:
            return "No file uploaded. Using sample data.", generate_sample_customer_data()
            
        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file.name)
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file.name)
            else:
                return "Unsupported file format. Please upload CSV or Excel file.", None
                
            return f"Successfully loaded data with {data.shape[0]} rows and {data.shape[1]} columns.", data
        except Exception as e:
            return f"Error loading file: {str(e)}", None
    
    def run_customer_analysis(data_csv, feature_cols_str, n_clusters):
        """Run customer segmentation analysis"""
        try:
            # Parse inputs
            if data_csv is None:
                return "No data available. Please upload a file or use sample data.", None, None, None
                
            # Parse feature columns
            feature_cols = [col.strip() for col in feature_cols_str.split(',')]
            
            # Initialize model
            customer_model = CustomerAnalysis(n_clusters=n_clusters)
            
            # Fit model
            customer_model.fit(data_csv, feature_cols=feature_cols)
            
            # Get cluster profiles
            profiles = customer_model.get_cluster_profiles()
            
            # Format profile data for display
            profile_display = pd.DataFrame({
                'Segment': profiles['name'],
                'Count': profiles['count'],
                'Percentage': profiles['percentage'].round(2)
            })
            
            # Add key stats for each feature
            for feature in feature_cols:
                profile_display[f'{feature} (avg)'] = profiles[f'{feature}_mean'].round(2)
            
            profile_html = profile_display.to_html(index=False)
            
            # Generate plot for the first two features
            fig1 = customer_model.plot_clusters(feature_cols[0], feature_cols[1])
            
            # Save plot to buffer
            buf1 = BytesIO()
            fig1.savefig(buf1, format='png')
            buf1.seek(0)
            plot1_base64 = base64.b64encode(buf1.read()).decode('utf-8')
            plt.close(fig1)
            
            # Generate feature importance plot
            fig2 = customer_model.plot_feature_importance()
            
            # Save plot to buffer
            buf2 = BytesIO()
            fig2.savefig(buf2, format='png')
            buf2.seek(0)
            plot2_base64 = base64.b64encode(buf2.read()).decode('utf-8')
            plt.close(fig2)
            
            # Return segmented data
            segments = customer_model.get_customer_segments()
            segments_display = segments[['customer_id', 'segment'] + feature_cols].head(50)
            
            return "Customer segmentation completed successfully!", profile_html, plot1_base64, plot2_base64, segments_display
            
        except Exception as e:
            return f"Error running model: {str(e)}", None, None, None, None
    
    with gr.Blocks() as customer_interface:
        gr.Markdown("# Customer Segmentation Analysis")
        
        with gr.Row():
            with gr.Column():
                data_file = gr.File(label="Upload Customer Data (CSV or Excel)")
                use_sample = gr.Button("Use Sample Data")
                data_info = gr.Textbox(label="Data Info", interactive=False)
                
                feature_cols = gr.Textbox(
                    label="Feature Columns (comma-separated)", 
                    value="age,income,tenure,purchases_last_year,avg_order_value,website_visits_last_month"
                )
                n_clusters = gr.Slider(
                    label="Number of Clusters", 
                    minimum=2, 
                    maximum=10, 
                    step=1, 
                    value=4
                )
                run_button = gr.Button("Run Customer Segmentation")
                
            with gr.Column():
                data_preview = gr.Dataframe(label="Data Preview")
        
        result = gr.Textbox(label="Result")
        
        with gr.Accordion("Model Results", open=False):
            with gr.Tabs():
                with gr.TabItem("Segment Profiles"):
                    segment_table = gr.HTML(label="Customer Segments")
                
                with gr.TabItem("Segment Visualization"):
                    segment_plot = gr.HTML(label="Customer Segments")
                    
                with gr.TabItem("Feature Importance"):
                    feature_plot = gr.HTML(label="Feature Importance")
                    
                with gr.TabItem("Segmented Customers"):
                    segments_data = gr.Dataframe(label="Segmented Customers (First 50)")
        
        def load_and_preview_data(file):
            message, data = load_data(file)
            return message, data if data is not None else None
        
        def use_sample_data():
            data = generate_sample_customer_data()
            return "Using sample data for Customer Analysis.", data
        
        data_file.upload(load_and_preview_data, inputs=[data_file], outputs=[data_info, data_preview])
        use_sample.click(use_sample_data, inputs=[], outputs=[data_info, data_preview])
        
        run_button.click(
            run_customer_analysis, 
            inputs=[data_preview, feature_cols, n_clusters], 
            outputs=[result, segment_table, segment_plot, feature_plot, segments_data]
        )
    
    return customer_interface

# Main Gradio interface for PyMC Marketing
def create_marketing_analytics_interface():
    """Create the main Gradio interface for marketing analytics"""
    
    with gr.Blocks(title="DMC Propaganda Marketing Analytics") as marketing_interface:
        gr.Markdown("# DMC Propaganda Marketing Analytics")
        gr.Markdown("Powered by PyMC Marketing")
        
        with gr.Tabs():
            with gr.TabItem("Media Mix Modeling"):
                mmm_interface = create_mmm_interface()
            
            with gr.TabItem("Customer Lifetime Value"):
                clv_interface = create_clv_interface()
                
            with gr.TabItem("Customer Segmentation"):
                customer_interface = create_customer_interface()
    
    return marketing_interface