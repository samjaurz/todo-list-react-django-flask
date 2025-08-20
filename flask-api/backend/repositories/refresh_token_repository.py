from backend.model.refresh_token import RefreshToken
from sqlalchemy.orm import Session
from typing import Type

class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_refresh_token(self, token_hash: str, user_agent: str, user_id: int):
        refresh_token = RefreshToken(
            token_hash=token_hash,
            user_agent=user_agent,
            user_id=user_id
        )
        self.session.add(refresh_token)
        self.session.commit()

        return refresh_token

    def get_refresh_token_by_user_id(self, user_id) :
        return self.session.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()

    def update_refresh_token(self, refresh_token_id: int, **kwargs) -> Type[RefreshToken] | None:
        refresh_token = self.session.query(RefreshToken).filter_by(id=refresh_token_id).first()
        if not refresh_token:
            return None
        required_fields = [
            "token_hash",
            "user_agent",
        ]
        updated = False
        for key, value in kwargs.items():
            if key in required_fields:
                setattr(refresh_token, key, value)
                updated = True
        if updated:
            self.session.commit()
        return refresh_token
