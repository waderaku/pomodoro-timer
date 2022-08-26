import os
from pathlib import Path

import inject
from chalice import Chalice

from src.domain.repository.auth_user_repository import AuthUserRepository
from src.domain.repository.task_user_repository import TaskUserRepository
from src.domain.repository.token_user_repository import TokenUserRepository
from src.domain.repository.user_repository import UserRepository
from src.infrastructure.dynamodb.repository.auth_user_dynamo_repository import (
    AuthUserDynamoRepository,
)
from src.infrastructure.dynamodb.repository.task_user_dynamo_repository import (
    TaskUserDynamoRepository,
)
from src.infrastructure.dynamodb.repository.token_user_dynamo_repository import (
    TokenUserDynamoRepository,
)
from src.infrastructure.dynamodb.repository.user_dynamo_repository import (
    UserDynamoRepository,
)
from src.urls import app_routing
from src.util import load_env

app = Chalice(app_name="backend")


def inject_config(binder: inject.Binder):
    binder.bind(UserRepository, UserDynamoRepository())
    binder.bind(TaskUserRepository, TaskUserDynamoRepository())
    binder.bind(AuthUserRepository, AuthUserDynamoRepository())
    binder.bind(TokenUserRepository, TokenUserDynamoRepository())


if os.environ.get("ENV", "") == "dev":
    load_env(Path().joinpath("src", ".env"))

inject.configure(inject_config)

app_routing(app)
