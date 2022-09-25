from abc import ABC, abstractmethod

from chalicelib.domain.model.entity.event import Event


class EventRepository(ABC):
    @abstractmethod
    def register_event(self, event: Event):
        raise NotImplementedError

    @abstractmethod
    def fetch_by_user_id(self, user_id: str) -> list[Event]:
        raise NotImplementedError

    @abstractmethod
    def update_event(self, event: Event):
        raise NotImplementedError
