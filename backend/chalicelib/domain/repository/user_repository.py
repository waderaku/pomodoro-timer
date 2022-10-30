from abc import ABC, abstractmethod
from typing import Optional

from chalicelib.domain.model.entity.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """ユーザIDに紐づくユーザを取得する.
        対象のユーザが存在しない場合、nullを返却する

        Args:
            user_id (str): ユーザID

        Returns:
            Optional[User]: 取得したユーザ
        """
        raise NotImplementedError()
