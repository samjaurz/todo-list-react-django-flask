from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.model import Base as MainBase

DATABASE_URL = "postgresql://root:root@localhost:5433/todo_list"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = MainBase

