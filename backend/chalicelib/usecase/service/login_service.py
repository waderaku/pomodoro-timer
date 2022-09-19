from typing import Optional

import inject
from chalicelib.domain.exception.custom_exception import NoExistUserException
from chalicelib.domain.model.entity.authorizer import PasswordAuthorizer
from chalicelib.domain.model.entity.token_user import TokenAuthorizer
from chalicelib.domain.model.value.password import Password
from chalicelib.domain.repository.auth_user_repository import (
    PasswordAuthorizerRepository,
)
from chalicelib.domain.repository.token_user_repository import TokenUserRepository


@inject.params(
    auth_user_repository=PasswordAuthorizerRepository,
    token_user_repository=TokenUserRepository,
)
def login_service(
    user_id: str,
    password: str,
    auth_user_repository: Optional[PasswordAuthorizerRepository] = None,
    token_user_repository: Optional[TokenUserRepository] = None,
) -> TokenAuthorizer:
    user = auth_user_repository.find_by_id(user_id)
    if not user:
        raise NoExistUserException()

    # user認証
    auth_user = PasswordAuthorizer(user_id=user_id, password=Password(password, False))
    user.authenticate(auth_user)

    # token生成
    token_user = TokenAuthorizer.create(user_id=user_id)

    # トークン登録
    token_user_repository.register_token(token_user)

    return token_user
