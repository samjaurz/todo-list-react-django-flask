import pytest
from backend.db_session import SessionLocal
session = SessionLocal()

@pytest.fixture(scope='function')
def app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@localhost:5433/todo_list_test"

    with app.app_context():
        db.create_all()

        yield db.session

        db.session.rollback()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()