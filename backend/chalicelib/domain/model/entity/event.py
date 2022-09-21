from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class Event:
    event_id: str
    task_id: str
    start: datetime
    end: datetime

    @classmethod
    def create(cls, task_id: str, start: datetime, end: datetime) -> Event:
        event_id = str(uuid4())
        return cls(event_id, task_id, start, end)
