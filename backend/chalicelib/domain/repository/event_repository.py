from abc import ABC, abstractmethod

from chalicelib.domain.model.entity.event import Event


class EventRepository(ABC):
    @abstractmethod
    def register_event(self, event: Event):
        raise NotImplementedError
