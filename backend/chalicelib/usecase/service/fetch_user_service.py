import inject
from chalicelib.domain.exception.custom_exception import NoExistUserException
from chalicelib.domain.model.entity.user import User
from chalicelib.domain.repository.repository import Repository


@inject.params(repository=Repository)
def fetch_user_service(user_id: str, repository: Repository) -> User:
    # TODO Docstring

    """ユーザIDに紐づくユーザ情報を取得する

    Args:
        user_repository (UserRepository): ユーザ情報についてDBとやり取りを行うリポジトリ
        user_id (str): ユーザID

    Raises:
        NoExistUserException: 対象のユーザが存在しないことを示す例外

    Returns:
        User: 取得したユーザ
    """
    user = repository.user_repository.find_by_id(user_id=user_id)
    if not user:
        raise NoExistUserException()
    return user
