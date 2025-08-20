import datetime
from sqlalchemy import String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from . import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id : Mapped[int] = mapped_column(primary_key=True)
    token_hash : Mapped[str] = mapped_column(String)
    user_agent: Mapped[str] = mapped_column(String)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return (f"<RefreshToken(id={self.id}, "
                f"token_hash={self.token_hash}, "
                f"user_agent={self.user_agent}, "
                f"user_id={self.user_id})>")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "token_hash": self.token_hash,
            "user_agent": self.user_agent,
            "user_id": self.user_id
        }

