from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable or use a default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Create the database engine with proper SSL and connection settings
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    # Additional connection parameters for PostgreSQL/NeonDB
    connect_args={
        "connect_timeout": 10,
    } if DATABASE_URL.startswith("postgresql") else {}
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session