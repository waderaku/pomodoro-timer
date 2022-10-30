from __future__ import annotations

from chalicelib.domain.exception.custom_exception import MissMatchPasswordException
from chalicelib.domain.model.value.password import Password


class AuthInfo:
    def __init__(self, user_id: str, password: Password):
        self._user_id = user_id
        self._password = password

    @classmethod
    def create(cls, user_id: str, plain_password: str) -> AuthInfo:
        hashed_password = Password(value=plain_password, is_hashed=False)
        return cls(user_id, hashed_password)

    def authenticate(self, other: AuthInfo):
        if self._user_id != other._user_id or self._password != other._password:
            raise MissMatchPasswordException()
