import traceback

from chalice import Response
from chalice.app import Request
from src.domain.exception.custom_exception import (
    MissMatchPasswordException,
    NoExistUserException,
    PasswordIsInvalidException,
)
from src.usecase.service.login_service import login_service


def login(request: Request):
    try:
        body = request.json_body
        token_user = login_service(user_id=body["userId"], password=body["password"])
        return Response(body=token_user._auth_token.value, status_code=200)
    except (
        NoExistUserException,
        PasswordIsInvalidException,
        MissMatchPasswordException,
    ):
        traceback.print_exc()
        return Response(body="ユーザIDもしくはパスワードが違います", status_code=400)
