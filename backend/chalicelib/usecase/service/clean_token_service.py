from typing import Optional

import inject
from chalicelib.domain.model.value.auth_token import AuthToken
from chalicelib.domain.repository.repository import Repository


@inject.params(repository=Repository)
def clean_token_service(
    repository: Repository,
) -> Optional[list[AuthToken]]:
    # TODO Docstring
    auth_token_repository = repository.auth_token_repository
    auth_token_list = auth_token_repository.find_all()
    expired_token_list = [
        auth_token for auth_token in auth_token_list if auth_token.is_expired()
    ]
    auth_token_repository.delete_token_list(expired_token_list)
    return expired_token_list
