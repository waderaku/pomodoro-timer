import inject
from chalicelib.domain.exception.custom_exception import (
    ExpiredTokenException,
    NoExistTokenException,
)
from chalicelib.domain.repository.repository import Repository


@inject.params(repository=Repository)
def authorize_service(
    token: str,
    repository: Repository,
) -> str:
    # TODO Docstring
    auth_token_repository = repository.auth_token_repository
    token_user = auth_token_repository.find_token_user_by_token(token)

    if not token_user:
        raise NoExistTokenException()

    if token_user.is_expired():
        auth_token_repository.delete_by_token(token)
        raise ExpiredTokenException()

    return token_user
