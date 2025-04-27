import subprocess
import os
import sys
import time
import signal
import atexit

def start_fastapi_server():
    """Start the FastAPI backend server"""
    print("Starting FastAPI backend server...")
    fastapi_process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"],
        cwd="/workspaces/dmc-propaganda/src/fastapi",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Give it a moment to start
    time.sleep(2)
    
    # Check if the process is still running
    if fastapi_process.poll() is None:
        print("FastAPI server started successfully!")
    else:
        stdout, stderr = fastapi_process.communicate()
        print("Failed to start FastAPI server!")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        sys.exit(1)
    
    return fastapi_process

def start_gradio_server():
    """Start the Gradio server"""
    print("Starting Gradio server...")
    from app import demo
    
    # Launch Gradio app
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)

def cleanup(fastapi_process):
    """Cleanup function to kill FastAPI server when exiting"""
    if fastapi_process and fastapi_process.poll() is None:
        print("Shutting down FastAPI server...")
        fastapi_process.send_signal(signal.SIGTERM)
        fastapi_process.wait(timeout=5)  # Wait up to 5 seconds for graceful shutdown

if __name__ == "__main__":
    # Start FastAPI backend first
    fastapi_process = start_fastapi_server()
    
    # Register cleanup function
    atexit.register(cleanup, fastapi_process)
    
    # Then start Gradio
    start_gradio_server()