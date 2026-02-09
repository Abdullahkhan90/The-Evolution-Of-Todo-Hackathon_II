from app.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
    print("Server started successfully")