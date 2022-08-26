from pathlib import Path

import inject
from chalice import Chalice

from chalicelib.domain.repository.auth_user_repository import \
    AuthUserRepository
from chalicelib.domain.repository.task_user_repository import \
    TaskUserRepository
from chalicelib.domain.repository.token_user_repository import \
    TokenUserRepository
from chalicelib.domain.repository.user_repository import UserRepository
from chalicelib.infrastructure.dynamodb.repository.auth_user_dynamo_repository import \
    AuthUserDynamoRepository
from chalicelib.infrastructure.dynamodb.repository.task_user_dynamo_repository import \
    TaskUserDynamoRepository
from chalicelib.infrastructure.dynamodb.repository.token_user_dynamo_repository import \
    TokenUserDynamoRepository
from chalicelib.infrastructure.dynamodb.repository.user_dynamo_repository import \
    UserDynamoRepository
from chalicelib.urls import app_routing
from chalicelib.util import load_env

app = Chalice(app_name="backend")


def inject_config(binder: inject.Binder):
    binder.bind(UserRepository, UserDynamoRepository())
    binder.bind(TaskUserRepository, TaskUserDynamoRepository())
    binder.bind(AuthUserRepository, AuthUserDynamoRepository())
    binder.bind(TokenUserRepository, TokenUserDynamoRepository())

if os.environ.get("ENV", "") == "dev":
    load_env(Path().joinpath("chalicelib", ".env"))

inject.configure(inject_config)

app_routing(app)
