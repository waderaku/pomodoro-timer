from typing import Optional

from chalicelib.domain.model.entity.user import User
from chalicelib.domain.repository.user_repository import UserRepository
from chalicelib.infrastructure.dynamodb.model.user_model import UserModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_io import DynamoIO
from chalicelib.infrastructure.dynamodb.repository.dynamo_key import DynamoKey


class UserDynamoRepository(UserRepository):
    """DynamoDBに登録されているユーザとやり取りをするリポジトリの実装クラス"""

    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def find_by_id(self, user_id: str) -> Optional[User]:
        key = DynamoKey(user_id, "user")
        user = self._dynamo_io.get_item(key, UserModel)
        if user is not None:
            return user.to_user()
        else:
            return None
