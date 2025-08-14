import pytest
from backend.flask.app import create_app
from backend.model import Base
from backend.model.user import User
from backend.db_session import SessionFactory
import bcrypt


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    app.db_factory = SessionFactory(app.config['SQLALCHEMY_DATABASE_URI'])

    with app.app_context():
        Base.metadata.create_all(app.db_factory.engine)
        yield app
        Base.metadata.drop_all(app.db_factory.engine)

@pytest.fixture
def db_session(app):
    session = app.db_factory.SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_account_factory(db_session):
    def _create_user(commit=True):
        password_client = "12345678"
        hashed = bcrypt.hashpw(password_client.encode(), bcrypt.gensalt()).decode()

        user = User(
            name="Samuel",
            last_name="Jauregui",
            email="test_account@email.com",
            password=hashed,
            status=True,
        )
        db_session.add(user)
        db_session.commit()
        return {
            "user_id": user.id,
            "username": user.email,
        }
    return _create_user