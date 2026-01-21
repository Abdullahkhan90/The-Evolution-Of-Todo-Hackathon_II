#!/usr/bin/env python3
"""
Test server with error logging
"""
import uvicorn
from app.main import app
import threading
import time

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")

if __name__ == "__main__":
    print("Starting server on port 8001...")
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Server started. Waiting for requests...")
    try:
        time.sleep(10)  # Wait 10 seconds
        print("Timeout reached, exiting...")
    except KeyboardInterrupt:
        print("Interrupted by user")