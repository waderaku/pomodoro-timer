from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any, Optional

ROOT_TASK_ID = "root"
ROOT_TASK_NAME = "HOME"
ROOT_TASK_WORKLOAD = 105120000


@dataclass
class Task:
    user_id: str
    task_id: str
    parent_id: Optional[str]
    name: str
    shortcut_flg: bool
    children_task_id: list[str]
    done: bool
    finished_workload: int
    estimated_workload: int
    deadline: datetime
    notes: str

    @classmethod
    def create_root(cls, user_id: str) -> Task:
        return cls(
            user_id=user_id,
            task_id=ROOT_TASK_ID,
            parent_id=None,
            name=ROOT_TASK_NAME,
            shortcut_flg=False,
            children_task_id=[],
            done=False,
            finished_workload=ROOT_TASK_WORKLOAD,
            estimated_workload=ROOT_TASK_WORKLOAD,
            deadline="2200-12-31",
            notes="",
        )

    def update(
        self,
        /,
        **changes: dict[str:Any],
    ) -> Task:
        """指定されたフィールドが更新された'新しい'インスタンスをリターンする

        Returns:
            Task: 特定のフィールドが更新された新インスタンス
        """
        return replace(self, **changes)

    def is_root(self) -> bool:
        return self.parent_id is None
