import os
from pathlib import Path

import inject
from chalice import Chalice

from chalicelib.domain.repository.repository import Repository
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import (
    DynamoRepository,
)
from chalicelib.presentation.controller.authorize_controller import authorize
from chalicelib.urls import app_routing
from chalicelib.util import load_env

app = Chalice(app_name="backend")


def inject_config(binder: inject.Binder):
    repository = DynamoRepository()
    binder.bind(Repository, repository)


if os.environ.get("ENV", "") == "dev":
    load_env(Path().joinpath("chalicelib", ".env"))

inject.configure(inject_config)


@app.authorizer()
def authorizer(auth_request):
    return authorize(auth_request)


app_routing(app, authorizer)
