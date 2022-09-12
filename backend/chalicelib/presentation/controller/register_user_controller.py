import traceback
from typing import Optional

from chalice import Response
from chalice.app import Request
from chalicelib.domain.exception.custom_exception import (
    AlreadyExistUserException,
    PasswordIsInvalidException,
)
from chalicelib.usecase.service.register_user_service import register_user_service


def register_user(request: Request) -> Optional[Response]:
    body = request.json_body
    user_id = body["userId"]
    password = body["password"]
    try:
        register_user_service(user_id=user_id, password=password)
    except (AlreadyExistUserException, PasswordIsInvalidException) as e:
        traceback.print_exc()
        return Response(
            status_code=400, body=traceback.format_exception_only(type(e), e)
        )
