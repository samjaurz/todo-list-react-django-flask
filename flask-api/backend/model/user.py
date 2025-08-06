from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean

from . import Base, task


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    status: Mapped[bool] = mapped_column(Boolean)
    task: Mapped[list["Task"]] = relationship("Task", back_populates="user")

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name} last_name={self.last_name} status={self.status}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "status": self.status.__str__()
        }
