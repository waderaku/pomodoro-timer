from __future__ import annotations

from chalicelib.domain.model.entity.authorizer import AuthInfo
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.model.entity.user import User


class TaskUser:
    def __init__(self, auth_info: AuthInfo, user: User, task_list: list[Task]):
        self._auth_info = auth_info
        self._user = user
        self._task_list = task_list

    @classmethod
    def create(cls, user_id: str, password: str) -> TaskUser:
        """ユーザオブジェクトの新規作成をする.
        それに伴い、当該ユーザに紐づくrootタスクを作成する

        Args:
            user_id (str): 新規作成するユーザのID
            password(str): 新規作成するユーザのパスワード、Cognito連携時に削除

        Returns:
            TaskUser:新規作成されたユーザ、タスクの集約オブジェクト
        """
        task = Task.create_root(user_id=user_id)
        user = User.create(user_id)
        auth_info = AuthInfo.create(user_id=user_id, plain_password=password)
        task_user = cls(
            auth_info,
            user=user,
            task_list=[task],
        )
        return task_user
