import pytest
from backend.flask.app import create_app
from backend.flask.auth.auth_jwt import JWTAuth
from backend.model import Base
from backend.model.user import User
from backend.model.task import Task
from backend.db_session import SessionFactory
import bcrypt


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    app.db_factory = SessionFactory(app.config["SQLALCHEMY_DATABASE_URI"])

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
def admin_user_factory(db_session):
    def _create_user(status: bool = True):
        password_client = "12345678"
        hashed = bcrypt.hashpw(password_client.encode(), bcrypt.gensalt()).decode()

        user = User(
            name="test",
            last_name="account",
            email="test_account@email.com",
            password=hashed,
            status=status,
        )
        db_session.add(user)
        db_session.commit()
        return user.to_dict()

    return _create_user


@pytest.fixture
def gen_token(db_session, admin_user_factory):
    user = admin_user_factory()
    token = JWTAuth().get_access_token(
        {
            "user_id": user["id"],
            "email": user["email"],
        }
    )

    return {"user": user, "email": user["email"], "tokens": token}


@pytest.fixture
def task_factory(db_session, gen_token):
    def _create_task():
        user_id = gen_token["user"]["id"]
        task = Task(
            name="test_task",
            status=False,
            user_id=user_id,
        )
        db_session.add(task)
        db_session.commit()

        return {"task": task.to_dict(), "tokens": gen_token["tokens"]}

    return _create_task
