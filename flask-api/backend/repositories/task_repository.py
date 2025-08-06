from backend.model.task import Task
from sqlalchemy.orm import Session
from typing import Type


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, name: str, status: bool, user_id: int) -> Task:
        task = Task(
            name=name,
            status=status,
            user_id=user_id,
        )
        self.session.add(task)
        self.session.commit()
        return task

    def get_task_by_id(self, task_id: int) -> Type[Task] | None:
        return self.session.query(Task).filter_by(id=task_id).first()

    def get_all_tasks(self)-> list[Type[Task]] | None:
       return self.session.query(Task).order_by(Task.id).all()

    def get_task_by_name(self, name: str)-> list[Type[Task]] | None:
        return self.session.query(Task).filter(Task.name.ilike(f"%{name}%")).all()

    def update_task(self, task_id: int, **kwargs) -> Type[Task] | None:
        task = self.session.query(Task).filter_by(id=task_id).first()
        if not task:
            return None
        required_fields = [
            "name",
            "status",
            "user_id"
        ]

        updated = False
        for key, value in kwargs.items():
            if key in required_fields:
                setattr(task, key, value)
                updated = True
        if updated:
            self.session.commit()
        return task

    def delete_task(self, task_id: int)-> bool:
        task = self.session.query(Task).filter_by(id=task_id).first()
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False