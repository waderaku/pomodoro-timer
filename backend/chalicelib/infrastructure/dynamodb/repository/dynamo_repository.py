from __future__ import annotations

from chalicelib.domain.repository.repository import Repository
from chalicelib.domain.repository.task_repository import TaskRepository
from chalicelib.domain.repository.user_repository import UserRepository
from chalicelib.infrastructure.dynamodb.repository.auth_token_dynamo_repository import (
    AuthTokenDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.repository.dynamo_io import DynamoIO
from chalicelib.infrastructure.dynamodb.repository.event_dynamo_repository import (
    EventDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.repository.password_authorizer_dynamo_repository import (
    PasswordAuthorizerDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.repository.task_dynamo_repository import (
    TaskDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.repository.task_user_dynamo_repository import (
    TaskUserDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.repository.user_dynamo_repository import (
    UserDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.util.get_table import get_pomodoro_table


class DynamoRepository(Repository):
    """DynamoDBへアクセスするリポジトリ全般で行われる共通処理をまとめたクラス"""

    def __init__(self):
        """Repositoryのコンストラクタ.
        pomodoro-infoテーブルオブジェクトを生成する
        """
        table = get_pomodoro_table()
        self._io = DynamoIO(table)
        self._event_repository = EventDynamoRepository(self._io)
        self._task_repository = TaskDynamoRepository(self._io)
        self._password_authrizer_repository = PasswordAuthorizerDynamoRepository(
            self._io
        )
        self._auth_token_repository = AuthTokenDynamoRepository(self._io)
        self._user_repository = UserDynamoRepository(self._io)
        self._task_user_repository = TaskUserDynamoRepository(self._io)

    @property
    def task_repository(self) -> TaskRepository:
        return self._task_repository

    @property
    def event_repository(self) -> EventDynamoRepository:
        return self._event_repository

    @property
    def auth_token_repository(self) -> AuthTokenDynamoRepository:
        return self._auth_token_repository

    @property
    def password_authorizer_repository(self) -> PasswordAuthorizerDynamoRepository:
        return self._password_authrizer_repository

    @property
    def task_user_repository(self) -> TaskUserDynamoRepository:
        return self._task_user_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    def batch_writer(self) -> DynamoIO:
        return self._io
