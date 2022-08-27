from abc import ABC, abstractmethod

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
