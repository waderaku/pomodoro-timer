from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime

from chalicelib.domain.model.entity.event import Event


@dataclass
class EventDynamoModel:
    ID: str
    DataType: str
    DataValue: str
    EndTime: str

    @classmethod
    def create(
        cls, user_id: str, task_id: str, start: datetime, end: datetime
    ) -> EventDynamoModel:
        return cls(
            ID=f"{user_id}_event",
            DataType=start.isoformat(),
            DataValue=task_id,
            EndTime=end.isoformat(),
        )

    @classmethod
    def from_event(cls, event: Event) -> EventDynamoModel:
        return cls(
            ID=f"{event.user_id}_event",
            DataType=event.start.isoformat(),
            DataValue=event.task_id,
            EndTime=event.end.isoformat(),
        )

    def to_dynamo_input(self) -> dict:
        return asdict(self)
