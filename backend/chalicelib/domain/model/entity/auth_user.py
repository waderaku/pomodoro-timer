from __future__ import annotations

from typing import Optional

from chalicelib.domain.model.entity.authorizer import AuthInfo
from chalicelib.domain.model.entity.user import User
from chalicelib.domain.model.value.default_length import DefaultLength
from chalicelib.domain.model.value.google_config import GoogleConfig


class AuthUser:
    def __init__(self, auth_info: AuthInfo, user: User):
        self._auth_info = auth_info
        self._user = user

    @classmethod
    def create(cls, user_id: str, password: str) -> AuthUser:
        user = User.create(user_id)
        auth_info = AuthInfo.create(user_id=user_id, plain_password=password)

        return cls(auth_info, user)

    def update(
        self,
        is_google_linked: bool,
        default_length: DefaultLength,
        google_config: Optional[GoogleConfig],
    ):
        self._user.update(
            is_google_linked=is_google_linked,
            default_length=default_length,
            google_config=google_config,
        )
