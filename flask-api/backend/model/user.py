import datetime
from sqlalchemy import String, DateTime, Boolean, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    task: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", order_by="Task.id"
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"name={self.name}, "
            f"last_name={self.last_name}, "
            f"email={self.email}, "
            f"password={self.password}, "
            f"status={self.status}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "status": self.status,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
