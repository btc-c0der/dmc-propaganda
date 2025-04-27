import gradio as gr
import json
import requests
import os

# Import marketing models interface
from marketing_models.gradio_interface import create_marketing_analytics_interface

# Configure the backend API URL
API_URL = os.environ.get("API_URL", "http://localhost:3000/api")

def check_api_health():
    """Check if the API is available"""
    try:
        response = requests.get(f"{API_URL}", timeout=2)
        if response.status_code == 200:
            return True, "API is available"
        else:
            return False, f"API is not responding correctly: {response.status_code}"
    except requests.RequestException as e:
        return False, f"API is not available: {str(e)}"

def login(username, password):
    """Login function that connects to the FastAPI backend"""
    try:
        # Check API health first
        api_available, message = check_api_health()
        if not api_available:
            return message, ""
            
        response = requests.post(f"{API_URL}/auth/login", data={
            "username": username,  # FastAPI OAuth2 expects username field
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            user_data = data.get('data', {}).get('user', {})
            token = data.get('data', {}).get('token', '')
            return f"Login successful! Welcome {user_data.get('name', 'User')}", token
        else:
            error_msg = response.json().get('detail', response.json().get('message', 'Unknown error'))
            return f"Login failed: {error_msg}", ""
    except Exception as e:
        return f"Error: {str(e)}", ""

def get_clients(token):
    """Get clients from the backend API"""
    try:
        if not token:
            return "Please login first", []
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/clients", headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            clients = response_data.get('data', [])
            return "Clients retrieved successfully", clients
        else:
            error_msg = response.json().get('detail', response.json().get('message', 'Unknown error'))
            return f"Failed to retrieve clients: {error_msg}", []
    except Exception as e:
        return f"Error: {str(e)}", []

def get_campaigns(token, client_id=None):
    """Get campaigns from the backend API"""
    try:
        if not token:
            return "Please login first", []
        
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{API_URL}/campaigns"
        if client_id:
            # For FastAPI endpoint which expects client_id in path
            url = f"{API_URL}/campaigns/client/{client_id}"
            
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            campaigns = response_data.get('data', [])
            return "Campaigns retrieved successfully", campaigns
        else:
            error_msg = response.json().get('detail', response.json().get('message', 'Unknown error'))
            return f"Failed to retrieve campaigns: {error_msg}", []
    except Exception as e:
        return f"Error: {str(e)}", []

def get_analytics(token, campaign_id=None):
    """Get analytics from the backend API"""
    try:
        if not token:
            return "Please login first", []
        
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{API_URL}/analytics"
        if campaign_id:
            # FastAPI uses query parameter for campaign_id
            url = f"{url}?campaign_id={campaign_id}"
            
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            analytics = response_data.get('data', [])
            return "Analytics retrieved successfully", analytics
        else:
            error_msg = response.json().get('detail', response.json().get('message', 'Unknown error'))
            return f"Failed to retrieve analytics: {error_msg}", []
    except Exception as e:
        return f"Error: {str(e)}", []

# Create authentication interface
with gr.Blocks() as auth_interface:
    gr.Markdown("# DMC Propaganda Login")
    api_status = gr.Textbox(label="API Status", value="Checking API connection...", interactive=False)
    with gr.Row():
        username = gr.Textbox(label="Email")
        password = gr.Textbox(label="Password", type="password")
    login_btn = gr.Button("Login")
    result = gr.Textbox(label="Result")
    token = gr.Textbox(label="Token", visible=False)
    
    # Add function to check API health on load
    def update_api_status():
        available, message = check_api_health()
        if available:
            return "✅ API is available"
        else:
            return f"❌ API connection issue: {message}"
    
    # Update status when interface loads
    auth_interface.load(update_api_status, inputs=None, outputs=[api_status])
    
    login_btn.click(login, inputs=[username, password], outputs=[result, token])

# Create clients interface
with gr.Blocks() as clients_interface:
    gr.Markdown("# DMC Propaganda Clients")
    token_input = gr.Textbox(label="Enter your token", placeholder="Paste your token here")
    get_clients_btn = gr.Button("Get Clients")
    clients_result = gr.Textbox(label="Result")
    clients_list = gr.JSON(label="Clients")
    
    get_clients_btn.click(get_clients, inputs=[token_input], outputs=[clients_result, clients_list])

# Create campaigns interface
with gr.Blocks() as campaigns_interface:
    gr.Markdown("# DMC Propaganda Campaigns")
    with gr.Row():
        campaign_token = gr.Textbox(label="Enter your token", placeholder="Paste your token here")
        client_id = gr.Textbox(label="Client ID (Optional)", placeholder="Enter client ID to filter")
    get_campaigns_btn = gr.Button("Get Campaigns")
    campaigns_result = gr.Textbox(label="Result")
    campaigns_list = gr.JSON(label="Campaigns")
    
    get_campaigns_btn.click(get_campaigns, inputs=[campaign_token, client_id], outputs=[campaigns_result, campaigns_list])

# Create analytics interface
with gr.Blocks() as analytics_interface:
    gr.Markdown("# DMC Propaganda Analytics")
    with gr.Row():
        analytics_token = gr.Textbox(label="Enter your token", placeholder="Paste your token here")
        campaign_id = gr.Textbox(label="Campaign ID (Optional)", placeholder="Enter campaign ID to filter")
    get_analytics_btn = gr.Button("Get Analytics")
    analytics_result = gr.Textbox(label="Result")
    analytics_data = gr.JSON(label="Analytics Data")
    
    get_analytics_btn.click(get_analytics, inputs=[analytics_token, campaign_id], outputs=[analytics_result, analytics_data])

# Create marketing analytics interface
marketing_interface = create_marketing_analytics_interface()

# Create the main interface
demo = gr.TabbedInterface(
    [auth_interface, clients_interface, campaigns_interface, analytics_interface, marketing_interface],
    ["Login", "Clients", "Campaigns", "Basic Analytics", "Marketing Analytics"],
    title="DMC Propaganda Dashboard"
)

if __name__ == "__main__":
    # Show a loading message
    print("Starting DMC Propaganda Dashboard...")
    print("Checking API availability...")
    api_available, message = check_api_health()
    if not api_available:
        print(f"Warning: {message}")
        print("Some features may not work without API connection.")
    else:
        print("API connection successful!")
    
    print("Loading marketing models...")
    print("Starting Gradio server on port 7860...")
    demo.launch(server_port=7860, share=False)