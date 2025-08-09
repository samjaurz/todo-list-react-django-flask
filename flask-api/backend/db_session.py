from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.model import Base as MainBase
from functools import wraps

DATABASE_URL = "postgresql://root:root@localhost:5433/todo_list"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = MainBase
Base.metadata.create_all(bind=engine)


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def with_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = None
        try:
            session = next(get_db())
            return func(session, *args, **kwargs)
        finally:
            if session:
                session.close()

    return wrapper
