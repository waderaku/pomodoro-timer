from abc import ABC, abstractmethod
from typing import Optional

from chalicelib.domain.model.entity.token_user import TokenAuthorizer


class TokenUserRepository(ABC):
    @abstractmethod
    def register_token(self, token_user: TokenAuthorizer) -> TokenAuthorizer:
        """発行したトークンを追加登録する

        Args:
            token_user (str): トークンデータ
        """
        raise NotImplementedError()

    @abstractmethod
    def find_by_token(self, token: str) -> Optional[TokenAuthorizer]:
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
