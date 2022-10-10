from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from chalicelib.infrastructure.dynamodb.model.dynamo_model import DynamoModel

from chalicelib.domain.model.entity.token_user import TokenUser
from chalicelib.domain.model.value.auth_token import AuthToken


@dataclass
class TokenUserModel(DynamoModel):
    ID: str
    DataType: str
    DataValue: str
    Deadline: str

    @classmethod
    def from_token_user(cls, token_user: TokenUser) -> TokenUserModel:
        return cls(
            ID="token",
            DataType=token_user._auth_token.value,
            DataValue=token_user._user_id,
            Deadline=token_user._auth_token.deadline.isoformat(),
        )

    def to_token_user(self) -> TokenUser:
        auth_token = self.to_auth_token()
        return TokenUser(self.DataValue, auth_token)

    def to_auth_token(self) -> AuthToken:
        return AuthToken(self.DataType, datetime.fromisoformat(self.Deadline))
