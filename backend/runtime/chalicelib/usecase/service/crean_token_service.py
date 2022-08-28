from typing import Optional

import inject
from chalicelib.domain.model.value.auth_token import AuthToken
from chalicelib.domain.repository.auth_token_repository import \
    AuthTokenRepository


@inject.params(auth_token_repository=AuthTokenRepository)
def crean_token_service(auth_token_repository: AuthTokenRepository) -> Optional[list[AuthToken]]:
    auth_token_list = auth_token_repository.find_all()
    expired_token_list = [
        auth_token for auth_token in auth_token_list if auth_token.is_expired()
    ]
    if len(expired_token_list) == 0:
        return
    auth_token_repository.delete_token_list(expired_token_list)
    return expired_token_list
