from typing import Optional

from chalicelib.domain.model.entity.authorizer import AuthInfo
from chalicelib.domain.repository.password_authorizer_repository import (
    PasswordAuthorizerRepository,
)
from chalicelib.infrastructure.dynamodb.model.user_model import UserModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_key import DynamoKey
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import DynamoIO


class PasswordAuthorizerDynamoRepository(PasswordAuthorizerRepository):
    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def find_by_id(self, user_id: str) -> Optional[AuthInfo]:
        key = DynamoKey(user_id, "user")
        authInfo_dynamo = self._dynamo_io.get_item(key, UserModel)
        if authInfo_dynamo is not None:
            return authInfo_dynamo.to_auth_info()
        else:
            return None
