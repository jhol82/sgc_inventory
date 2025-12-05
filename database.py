import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load the DATABASE_URL from .env
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Provide a database session to routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
