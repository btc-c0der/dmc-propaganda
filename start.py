#!/usr/bin/env python3
"""
DMC Propaganda Startup Script
This script installs dependencies and starts the FastAPI backend and Gradio frontend.
"""
import os
import sys
import subprocess
import time

def install_dependencies():
    """Install required dependencies"""
    print("Installing FastAPI backend dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", 
        "src/fastapi/requirements.txt"
    ], check=True)
    
    print("Installing Gradio frontend dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", 
        "src/gradio/requirements.txt"
    ], check=True)
    
    print("Dependencies installed successfully!")

def setup_database():
    """Setup initial database configuration"""
    # Note: This would typically include database migration scripts
    # For now, we'll just print a message
    print("MongoDB will be connected when the application starts")
    print("Make sure MongoDB is running at the URI specified in .env")

def start_application():
    """Start the application using the Gradio server script"""
    print("Starting DMC Propaganda application...")
    subprocess.run([
        sys.executable, "src/gradio/server.py"
    ], check=True)

if __name__ == "__main__":
    print("DMC Propaganda Application Startup")
    print("==================================")
    
    try:
        install_dependencies()
        setup_database()
        start_application()
    except Exception as e:
        print(f"Error during startup: {e}")
        sys.exit(1)