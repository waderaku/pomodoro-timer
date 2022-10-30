from abc import ABC, abstractmethod
from typing import Optional

from chalicelib.domain.model.entity.auth_user import AuthUser


class AuthUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[AuthUser]:
        """ユーザIDに紐づく認証ユーザを取得する.
        対象のユーザが存在しない場合、nullを返却する

        Args:
            user_id (str): ユーザID

        Returns:
            Optional[AuthUser]: 取得した認証ユーザ
        """
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, auth_user: AuthUser):
        """登録されている認証ユーザを更新する

        Args:
            user (User): 更新するユーザ
        """
        raise NotImplementedError()
