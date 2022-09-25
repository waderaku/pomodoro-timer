from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from chalicelib.domain.model.entity.event import Event
from chalicelib.infrastructure.dynamodb.model.dynamo_model import DynamoModel


@dataclass
class EventInfo:
    event_id: str
    end: str


@dataclass
class EventDynamoModel(DynamoModel):
    ID: str
    DataType: str
    DataValue: str
    EventInfo: EventInfo

    @classmethod
    def from_event(cls, event: Event) -> EventDynamoModel:
        event_info = EventInfo(event.event_id, event.end.isoformat())
        return cls(
            ID=f"{event.user_id}_event",
            DataType=event.start.isoformat(),
            DataValue=event.task_id,
            EventInfo=event_info,
        )

    def to_event(self) -> Event:
        user_id = self.ID[:-6]
        event_id = self.EventInfo.event_id
        task_id = self.DataValue
        start = datetime.fromisoformat(self.DataType)
        end = datetime.fromisoformat(self.EventInfo.end)
        return Event(
            user_id=user_id, event_id=event_id, task_id=task_id, start=start, end=end
        )
