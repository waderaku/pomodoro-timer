import inject
from chalicelib.domain.exception.custom_exception import NoExistUserException
from chalicelib.domain.model.entity.authorizer import AuthInfo
from chalicelib.domain.model.entity.token_user import TokenUser
from chalicelib.domain.model.value.password import Password
from chalicelib.domain.repository.repository import Repository


@inject.params(
    repositor=Repository,
)
def login_service(
    user_id: str,
    password: str,
    repository: Repository,
) -> TokenUser:
    # TODO Docstring
    db_auth_info = repository.password_authorizer_repository.find_by_id(user_id)
    if not db_auth_info:
        raise NoExistUserException()

    # user認証
    auth_info = AuthInfo(user_id=user_id, password=Password(password, False))
    db_auth_info.authenticate(auth_info)

    # token生成
    token_user = TokenUser.create(user_id=user_id)

    # トークン登録
    repository.auth_token_repository.register_token(token_user)

    return token_user
