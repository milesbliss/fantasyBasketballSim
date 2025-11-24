from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fantasy.db"  # file lives in the repo workspace

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite + threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
