import pytest
from backend.flask.app import create_app
from backend.model import Base
from backend.model.user import User
from backend.db_session import engine, SessionLocal
import bcrypt

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield app
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture
def admin_account_factory(db_session):
    def _create_user():
        password_client = "12345678"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_client.encode("utf-8"), salt).decode("utf-8")

        user = User(
            name="Samuel",
            last_name="Jauregui",
            email="test_account@email.com",
            password=hashed,
            status= True,
        )
        db_session.add(user)
        db_session.commit()
        return user
    return _create_user

