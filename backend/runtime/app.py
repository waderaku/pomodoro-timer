import os
from pathlib import Path

import boto3
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
from chalicelib.util import load_env

app = Chalice(app_name='backend')
dynamodb = boto3.resource('dynamodb')
dynamodb_table = dynamodb.Table(os.environ.get('APP_TABLE_NAME', ''))

def inject_config(binder: inject.Binder):
    binder.bind(UserRepository, UserDynamoRepository())
    binder.bind(TaskUserRepository, TaskUserDynamoRepository())
    binder.bind(AuthUserRepository, AuthUserDynamoRepository())
    binder.bind(TokenUserRepository, TokenUserDynamoRepository())

load_env(Path().joinpath("chalicelib", ".env"))
inject.configure(inject_config)


@app.route('/users', methods=['POST'])
def create_user():
    request = app.current_request.json_body
    item = {
        'PK': 'User#%s' % request['username'],
        'SK': 'Profile#%s' % request['username'],
    }
    item.update(request)
    dynamodb_table.put_item(Item=item)
    return {}


@app.route('/users/{username}', methods=['GET'])
def get_user(username):
    key = {
        'PK': 'User#%s' % username,
        'SK': 'Profile#%s' % username,
    }
    item = dynamodb_table.get_item(Key=key)['Item']
    del item['PK']
    del item['SK']
    return item
