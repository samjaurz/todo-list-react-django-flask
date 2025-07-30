from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .task import Task
from .users import User