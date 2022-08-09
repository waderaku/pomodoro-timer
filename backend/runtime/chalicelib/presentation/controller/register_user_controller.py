import traceback

from chalicelib.domain.exception.custom_exception import (
    AlreadyExistUserException,
    PasswordIsInvalidException,
)
from chalicelib.presentation.http.request.auth_user_request import AuthUser
from chalicelib.usecase.service.register_user_service import register_user_service
from fastapi import HTTPException


async def register_user(request: AuthUser):
    try:
        register_user_service(user_id=request.userId, password=request.password)
    except (AlreadyExistUserException, PasswordIsInvalidException) as e:
        raise HTTPException(
            status_code=400, detail=traceback.format_exception_only(type(e), e)
        )
