from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable or use a default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session