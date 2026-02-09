from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks, users, todo, chat
from app.routers.auth import router
from app.core.auth import get_current_user
from app.database.init_db import create_db_and_tables
import os
from dotenv import load_dotenv

load_dotenv()

print("Creating FastAPI app...")
app = FastAPI(
    title="Todo API",
    description="A simple todo application API with user authentication",
    version="1.0.0"
)
print("FastAPI app created successfully")

# Get environment variables for CORS configuration
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
frontend_url = os.getenv("FRONTEND_URL", "")

# Build allowed origins list
allowed_origins = []

# Add explicitly configured origins
if allowed_origins_env:
    allowed_origins.extend([origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()])

# Add frontend URL if specified
if frontend_url:
    allowed_origins.append(frontend_url.strip())

# Add default development origins
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
allowed_origins.extend(default_origins)

# Remove duplicates
allowed_origins = list(set(allowed_origins))

# In production, also allow the environment variable or all origins if needed
if os.getenv("ENVIRONMENT", "development") == "production":
    # In production, only allow specific origins
    if not frontend_url:
        print("WARNING: FRONTEND_URL not set for production. Using localhost for development.")
else:
    # In development, be more permissive
    allowed_origins.append("*")

# Remove "*" if we have specific origins (cannot mix specific and wildcard)
if "*" in allowed_origins and len(allowed_origins) > 1:
    allowed_origins.remove("*")
    allowed_origins.append("*")  # Keep wildcard at end, will be only origin

print(f"Allowed CORS origins: {allowed_origins}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routers
print("Including routers...")
app.include_router(tasks.router, prefix="/api/users", tags=["tasks"])
print("Tasks router included")
app.include_router(users.router, prefix="/api/users", tags=["users"])
print("Users router included")
app.include_router(todo.router, prefix="/api/todos", tags=["todos"])
print("Todo router included")
app.include_router(chat.router, prefix="/api", tags=["chat"])
print("Chat router included")
app.include_router(router, prefix="/auth", tags=["auth"])
print("Auth router included")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

