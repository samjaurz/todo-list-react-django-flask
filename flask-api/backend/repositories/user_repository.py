from backend.model import Task
from backend.model.user import User
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Type


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, name: str, last_name: str, email: str, password: str, status: bool) -> User:
        now = datetime.now(timezone.utc)
        user = User(
            name=name,
            last_name=last_name,
            email=email,
            password=password,
            status=status,
            created_at=now,
            updated_at=now,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_id(self, user_id: int) -> Type[User] | None:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_email(self, user_email: str) -> Type[User] | None:
        return self.session.query(User).filter_by(email=user_email).first()

    def get_all_users(self) -> list[Type[User]] | None:
        return self.session.query(User).all()

    def get_all_tasks_by_user(self, user_id: int) -> list[Type[Task]] | None:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user is None:
            return None
        tasks = user.task
        return [task.to_dict() for task in tasks]

    def delete_user(self, user_id: int) -> bool:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
