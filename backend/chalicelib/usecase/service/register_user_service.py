from typing import Optional

import inject
from chalicelib.domain.exception.custom_exception import AlreadyExistUserException
from chalicelib.domain.model.entity.task_user import TaskUser
from chalicelib.domain.repository.repository import Repository


@inject.params(
    repository=Repository,
)
def register_user_service(
    user_id: str,
    password: str,
    repository: Repository,
):
    """新規にユーザーデータを登録する

    Args:
        user_id (str): ユーザーID
        password(str): パスワード、Cognito連携時に削除

    Raises:
        AlreadyExistUserException: 既に対象のユーザーが存在する場合に発行される例外
    """
    # 存在チェック
    if repository.user_repository.find_by_id(user_id=user_id):
        raise AlreadyExistUserException()

    # 新規登録
    task_user = TaskUser.create(user_id, password=password)
    repository.task_user_repository.register_task_user(task_user=task_user)
