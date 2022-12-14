from typing import Optional

import inject
from chalicelib.domain.exception.custom_exception import (
    ExpiredTokenException,
    NoExistTokenException,
)
from chalicelib.domain.model.entity.token_user import TokenUser
from chalicelib.domain.repository.token_user_repository import TokenUserRepository


@inject.params(token_user_repository=TokenUserRepository)
def authorize_service(
    token: str,
    token_user_repository: Optional[TokenUserRepository] = None,
) -> TokenUser:
    token_user = token_user_repository.find_by_token(token)

    if not token_user:
        raise NoExistTokenException()

    if token_user.is_expired():
        token_user_repository.delete_by_token(token)
        raise ExpiredTokenException()

    return token_user
