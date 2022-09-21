from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class Event:
    user_id: str
    event_id: str
    task_id: str
    start: datetime
    end: datetime

    @classmethod
    def create(
        cls, user_id: str, task_id: str, start: datetime, end: datetime
    ) -> Event:
        event_id = str(uuid4())
        return cls(
            user_id=user_id, event_id=event_id, task_id=task_id, start=start, end=end
        )
