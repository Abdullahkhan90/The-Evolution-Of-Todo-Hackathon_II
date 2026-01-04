from sqlmodel import SQLModel
from app.database.database import engine

def create_db_and_tables():
    """
    Create database tables if they don't exist.
    """
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Database tables created successfully!")