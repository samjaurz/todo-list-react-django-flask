import pytest
from backend.flask.app import create_app
from backend.db_session import Base, engine, SessionLocal

@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app

@pytest.fixture(scope='function')
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)
    Base.metadata.create_all(bind=connection)

    yield session

    transaction.rollback()
    session.rollback()
    session.close()
    connection.close()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
