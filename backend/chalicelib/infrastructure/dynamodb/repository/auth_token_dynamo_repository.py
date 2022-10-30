from typing import Optional

from boto3.dynamodb.conditions import Key
from chalicelib.domain.model.entity.token_user import TokenUser
from chalicelib.domain.model.value.auth_token import AuthToken
from chalicelib.domain.repository.auth_token_repository import AuthTokenRepository
from chalicelib.infrastructure.dynamodb.model.token_user_model import TokenUserModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_io import DynamoIO
from chalicelib.infrastructure.dynamodb.repository.dynamo_key import DynamoKey


class AuthTokenDynamoRepository(AuthTokenRepository):
    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def find_all(self) -> list[AuthToken]:
        condition = Key("ID").eq("token")
        auth_token_dynamo_list = self._dynamo_io.query(condition, TokenUserModel)
        return [dynamo_model.to_auth_token() for dynamo_model in auth_token_dynamo_list]

    def register_token(self, token_user: TokenUser):
        dynamo_model = TokenUserModel.from_token_user(token_user)
        self._dynamo_io.put_item(dynamo_model)

    def delete_token_list(self, token_list: list[AuthToken]):
        for token in token_list:
            key = DynamoKey("token", token.value)
            self._dynamo_io.delete_item(key)

    def find_token_user_by_token(self, token: str) -> Optional[TokenUser]:
        key = DynamoKey("token", token)
        token_user_dynamo = self._dynamo_io.get_item(key, TokenUserModel)

        if token_user_dynamo is not None:
            return token_user_dynamo.to_token_user()
        else:
            return None

    def delete_by_token(self, token: str):
        key = DynamoKey("token", token)
        self._dynamo_io.delete_item(key)
