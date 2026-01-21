#!/usr/bin/env python3
"""
Simple server to test the chat endpoint
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting server on port 8001...")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)