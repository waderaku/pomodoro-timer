from abc import ABC, abstractmethod

from chalicelib.domain.model.entity.authorizer import AuthInfo


class PasswordAuthorizerRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> AuthInfo:
        """認証ユーザデータを取得する

        Args:
            user_id (str): ユーザID
        """
        raise NotImplementedError()
