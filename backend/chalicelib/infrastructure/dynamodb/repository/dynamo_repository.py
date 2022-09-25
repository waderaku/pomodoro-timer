from __future__ import annotations

from chalicelib.domain.repository.auth_token_repository import AuthTokenRepository
from chalicelib.domain.repository.auth_user_repository import (
    PasswordAuthorizerRepository,
)
from chalicelib.domain.repository.repository import Repository
from chalicelib.domain.repository.task_repository import TaskRepository
from chalicelib.domain.repository.user_repository import UserRepository
from chalicelib.infrastructure.dynamodb.repository.dynamo_io import DynamoIO
from chalicelib.infrastructure.dynamodb.repository.event_dynamo_repository import (
    EventDynamoRepository,
)
from chalicelib.infrastructure.dynamodb.repository.task_dynamo_repository import (
    TaskDynamoRepository,
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

    @property
    def task_repository(self) -> TaskRepository:
        return self._task_repository

    @property
    def event_repository(self) -> EventDynamoRepository:
        return self._event_repository

    @property
    def auth_token_repository(self) -> AuthTokenRepository:
        raise NotImplementedError

    @property
    def password_authorizer_repository(self) -> PasswordAuthorizerRepository:
        raise NotImplementedError

    @property
    def user_repository(self) -> UserRepository:
        raise NotImplementedError

    def batch_writer(self) -> DynamoIO:
        return self._io
