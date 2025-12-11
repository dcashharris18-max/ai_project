import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

try:
    engine = create_engine(DATABASE_URL, future=True)
except Exception:
    # If the configured DB driver is unavailable (e.g., psycopg2 missing),
    # fall back to a local sqlite DB for tests and local development.
    # This keeps test collection runnable in constrained environments.
    fallback_url = "sqlite:///./test.db"
    engine = create_engine(fallback_url, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
