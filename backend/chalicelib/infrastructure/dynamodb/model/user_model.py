from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from chalicelib.domain.model.entity.auth_user import AuthUser
from chalicelib.domain.model.entity.authorizer import AuthInfo
from chalicelib.domain.model.entity.user import User
from chalicelib.domain.model.value.default_length import DefaultLength
from chalicelib.domain.model.value.google_config import Calendar, GoogleConfig, TaskList
from chalicelib.domain.model.value.password import Password
from chalicelib.infrastructure.dynamodb.model.dynamo_model import DynamoModel


@dataclass
class UserInfoModel:
    is_google_linked: bool
    default_length: dict
    google_config: Optional[dict] = None
    password: Optional[str] = None


@dataclass
class UserModel(DynamoModel):
    ID: str
    UserInfo: UserInfoModel
    DataType: str = "user"

    def to_user(self) -> User:
        """ドメインのユーザオブジェクトに変換する

        Returns:
            User: 変換したユーザオブジェクト
        """
        user_info = self.UserInfo
        default_length = DefaultLength(
            work=int(user_info.default_length["work"]),
            rest=int(user_info.default_length["rest"]),
        )

        google_config = None
        if user_info.google_config:
            google_config = GoogleConfig(
                Calendar(**user_info.google_config["calendar"]),
                TaskList(**user_info.google_config["task_list"]),
            )
        return User(
            user_id=self.ID,
            is_google_linked=user_info.is_google_linked,
            default_length=default_length,
            google_config=google_config,
        )

    def to_auth_info(self) -> AuthInfo:
        """認証用ユーザを生成する

        Returns:
            AuthUser: 認証用ユーザ
        """
        return AuthInfo(
            user_id=self.ID, password=Password(self.UserInfo.password, True)
        )

    def to_auth_user(self) -> AuthUser:
        user_info = self.UserInfo
        default_length = DefaultLength(
            work=int(user_info.default_length["work"]),
            rest=int(user_info.default_length["rest"]),
        )
        google_config = None
        if user_info.google_config:
            google_config = GoogleConfig(
                Calendar(**user_info.google_config["calendar"]),
                TaskList(**user_info.google_config["task_list"]),
            )

        user = User(
            user_id=self.ID,
            is_google_linked=user_info.is_google_linked,
            default_length=default_length,
            google_config=google_config,
        )

        auth_info = AuthInfo(
            user_id=self.ID, password=Password(self.UserInfo.password, True)
        )

        return AuthUser(auth_info, user)

    @classmethod
    def from_user_and_auth_info(cls, user: User, auth_info: AuthInfo) -> UserModel:
        """ドメインのユーザオブジェクトをDBに登録する形式に変換する

        Args:
            user (User): ユーザオブジェクト
        """
        user_info_model = UserInfoModel(
            is_google_linked=user._is_google_linked,
            google_config=None
            if not user._google_config
            else asdict(user._google_config),
            default_length=asdict(user._default_length),
            password=auth_info._password.value,
        )
        return cls(ID=user._user_id, UserInfo=user_info_model)
