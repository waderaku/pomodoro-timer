from __future__ import annotations

from src.domain.exception.custom_exception import MissMatchPasswordException
from src.domain.model.value.password import Password


class AuthUser:
    def __init__(self, user_id: str, password: Password):
        self._user_id = user_id
        self._password = password

    def authenticate(self, other: AuthUser):
        if self._user_id != other._user_id or self._password != other._password:
            raise MissMatchPasswordException()
