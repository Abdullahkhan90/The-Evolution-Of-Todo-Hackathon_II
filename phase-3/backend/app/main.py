from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks, users, todo, chat
from app.core.auth import get_current_user
from app.database.init_db import create_db_and_tables
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Todo API",
    description="A simple todo application API with user authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # Allow frontend origin and all during testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routers
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(todo.router, prefix="/api/todos", tags=["todos"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}