import traceback

from chalice import AuthResponse
from chalice.app import AuthRequest
from src.domain.exception.custom_exception import (
    ExpiredTokenException,
    NoExistTokenException,
)
from src.usecase.service.authorize_service import authorize_service


def authorize(request: AuthRequest) -> AuthResponse:
    try:
        token_user = authorize_service(request.token)
        return AuthResponse(
            routes=["*"], principal_id="user", context={"user_id": token_user._user_id}
        )
    except (NoExistTokenException, ExpiredTokenException):
        traceback.print_exc()
        return AuthResponse(routes=[], principal_id="user")
