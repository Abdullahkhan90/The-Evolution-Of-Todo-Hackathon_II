import sys
import os
import traceback
from app.main import app
import uvicorn

def run_server():
    try:
        print("Starting server on http://127.0.0.1:8000")
        print("Press Ctrl+C to stop the server")
        
        # Initialize the database
        from app.database.init_db import create_db_and_tables
        print("Initializing database tables...")
        create_db_and_tables()
        print("Database initialized successfully")
        
        # Run the server
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000, 
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run_server()