from abc import ABC, abstractmethod
from typing import Optional

from chalicelib.domain.model.entity.token_user import TokenUser
from chalicelib.domain.model.value.auth_token import AuthToken


class AuthTokenRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[AuthToken]:
        """認証トークンデータを全て取得する"""
        raise NotImplementedError()

    @abstractmethod
    def delete_token_list(self, token_list: list[AuthToken]):
        """トークン一覧をすべて削除する

        Args:
            token_list (list[AuthToken]): 削除対象のトークン一覧
        """
        raise NotImplementedError()

    @abstractmethod
    def find_token_user_by_token(self, token: str) -> Optional[TokenUser]:
        """トークンに紐づくデータを取得する

        Args:
            token (str): トークン

        Returns:
            TokenUser: トークンデータ
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_by_token(self, token: str):
        """トークンに紐づくデータを削除する

        Args:
            token (str): トークン

        Returns:
            TokenUser: トークンデータ
        """
        raise NotImplementedError()

    @abstractmethod
    def register_token(self, token_user: TokenUser):
        """発行したトークンを追加登録する

        Args:
            token_user (str): トークンデータ
        """
        raise NotImplementedError()
