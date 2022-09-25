from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
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

    def update_task_id(self, task_id: str) -> Event:
        """指定されたフィールドが更新された'新しい'インスタンスをリターンする

        Returns:
            Task: 特定のフィールドが更新された新インスタンス
        """
        return replace(self, task_id=task_id)
