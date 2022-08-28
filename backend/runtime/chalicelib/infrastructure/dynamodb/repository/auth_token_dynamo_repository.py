from boto3.dynamodb.conditions import Key
from chalicelib.domain.model.value.auth_token import AuthToken
from chalicelib.domain.repository.auth_token_repository import AuthTokenRepository
from chalicelib.infrastructure.dynamodb.model.token_user_model import TokenUserModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import (
    DynamoRepository,
)


class AuthTokenDynamoRepository(AuthTokenRepository, DynamoRepository):
    def find_all(self) -> list[AuthToken]:
        item_list = self._table.query(KeyConditionExpression=Key("ID").eq("token"))[
            "Items"
        ]
        return [TokenUserModel(**item).to_auth_token() for item in item_list]

    def delete_token_list(self, token_list: list[AuthToken]):
        with self._table.batch_writer() as batch:
            for token in token_list:
                batch.delete_item(Key={"ID": "token", "DataType": token.value})
