from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import  String, Boolean

from . import Base

class Task(Base):
    __tablename__ = "task"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String)
    status : Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<Task id={self.id} name={self.name}>"


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.__str__(),
        }
