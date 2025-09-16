from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.model import Base
from functools import wraps
from flask import current_app


class SessionFactory:
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(self.engine)

    def get_db(self):
        database = self.SessionLocal()
        try:
            yield database
        finally:
            database.close()


def with_db_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        db_gen = current_app.db_factory.get_db()
        session = next(db_gen)
        try:
            return f(session, *args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            try:
                next(db_gen)
            except StopIteration:
                pass

    return wrapper
