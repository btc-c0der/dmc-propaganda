import subprocess
import os
import sys
import time
import signal
import atexit

def start_nodejs_server():
    """Start the Node.js backend server"""
    print("Starting Node.js backend server...")
    node_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="/workspaces/dmc-propaganda",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Give it a moment to start
    time.sleep(2)
    
    # Check if the process is still running
    if node_process.poll() is None:
        print("Node.js server started successfully!")
    else:
        stdout, stderr = node_process.communicate()
        print("Failed to start Node.js server!")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        sys.exit(1)
    
    return node_process

def start_gradio_server():
    """Start the Gradio server"""
    print("Starting Gradio server...")
    from app import demo
    
    # Launch Gradio app
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)

def cleanup(node_process):
    """Cleanup function to kill Node.js server when exiting"""
    if node_process and node_process.poll() is None:
        print("Shutting down Node.js server...")
        node_process.send_signal(signal.SIGTERM)
        node_process.wait(timeout=5)  # Wait up to 5 seconds for graceful shutdown

if __name__ == "__main__":
    # Start Node.js backend first
    node_process = start_nodejs_server()
    
    # Register cleanup function
    atexit.register(cleanup, node_process)
    
    # Then start Gradio
    start_gradio_server()