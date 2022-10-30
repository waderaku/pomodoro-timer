from chalicelib.domain.model.entity.auth_user import AuthUser
from chalicelib.domain.repository.auth_user_repository import AuthUserRepository
from chalicelib.infrastructure.dynamodb.model.user_model import UserModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_io import DynamoIO
from chalicelib.infrastructure.dynamodb.repository.dynamo_key import DynamoKey


class AuthUserDynamoRepository(AuthUserRepository):
    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def find_by_id(self, user_id: str):
        key = DynamoKey(user_id, "user")
        auth_user_dynamo = self._dynamo_io.get_item(key, UserModel)
        if auth_user_dynamo is not None:
            return auth_user_dynamo.to_auth_user()
        else:
            return None

    def update_user(self, auth_user: AuthUser):
        dynamo_model = UserModel.from_user_and_auth_info(
            auth_user._user, auth_user._auth_info
        )
        self._dynamo_io.put_item(dynamo_model)
