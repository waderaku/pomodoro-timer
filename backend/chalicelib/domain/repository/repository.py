from __future__ import annotations

from abc import ABC, abstractmethod

from chalicelib.domain.repository.auth_token_repository import AuthTokenRepository
from chalicelib.domain.repository.auth_user_repository import (
    PasswordAuthorizerRepository,
)
from chalicelib.domain.repository.event_repository import EventRepository
from chalicelib.domain.repository.task_repository import TaskRepository
from chalicelib.domain.repository.user_repository import UserRepository


class Repository(ABC):
    @property
    @abstractmethod
    def task_repository(self) -> TaskRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def event_repository(self) -> EventRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def auth_token_repository(self) -> AuthTokenRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def password_authorizer_repository(self) -> PasswordAuthorizerRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def user_repository(self) -> UserRepository:
        raise NotImplementedError

    @abstractmethod
    def batch_writer(self) -> BatchWriter:
        raise NotImplementedError


class BatchWriter:
    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self):
        raise NotImplementedError