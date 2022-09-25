from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from uuid import uuid4

from chalicelib.domain.exception.custom_exception import (
    AlreadyDoneParentTaskException,
    NotShortcutTaskException,
)

ROOT_TASK_ID = "root"
ROOT_TASK_NAME = "HOME"
ROOT_TASK_ESTIMATED_WORKLOAD = timedelta(days=200 * 365)
ROOT_TASK_INITIAL_WORKLOAD = timedelta(days=0)
ROOT_TASK_PARENT_ID = ""


@dataclass(frozen=True)
class Task:
    """タスクドメイン"""

    user_id: str
    task_id: str
    name: str
    shortcut_flg: bool
    children_task_id: list[str]
    parent_id: str
    event_id_list: list[str]
    done: bool
    finished_workload: timedelta
    estimated_workload: timedelta
    deadline: datetime
    notes: str

    def __post_init__(self):
        # rootの子タスクの場合shortcut_flgがtrueであること
        if self.parent_id == ROOT_TASK_ID and not self.shortcut_flg:
            raise NotShortcutTaskException()

    @classmethod
    def create(
        cls,
        user_id: str,
        name: str,
        parent_id: str,
        estimated_workload: int,
        deadline: datetime,
        notes: str,
        shortcut_flg: bool,
    ):
        task_id = str(uuid4())
        done = False
        event_id_list = list()
        children_id_list = list()
        finished_workload = 0.0
        return Task(
            user_id=user_id,
            task_id=task_id,
            name=name,
            shortcut_flg=shortcut_flg,
            children_task_id=children_id_list,
            parent_id=parent_id,
            event_id_list=event_id_list,
            done=done,
            finished_workload=finished_workload,
            estimated_workload=estimated_workload,
            deadline=deadline,
            notes=notes,
        )

    @classmethod
    def create_root(cls, user_id: str) -> Task:
        """ルートタスクのドメインオブジェクトを作成するファクトリ関数

        Args:
            user_id (str): ユーザID

        Returns:
            Task: 作成したルートタスクのドメイン
        """
        return cls(
            user_id=user_id,
            task_id=ROOT_TASK_ID,
            name=ROOT_TASK_NAME,
            shortcut_flg=False,
            children_task_id=[],
            done=False,
            parent_id=ROOT_TASK_PARENT_ID,
            event_id_list=[],
            finished_workload=ROOT_TASK_INITIAL_WORKLOAD,
            estimated_workload=ROOT_TASK_ESTIMATED_WORKLOAD,
            deadline="2200-12-31",
            notes="",
        )

    def add_workload(
        self,
        workload: timedelta,
    ) -> Task:
        """
        Returns:
            Task: finished_workloadフィールドがworkloadだけ加算された新インスタンス
        """
        return self.update_workload(self.finished_workload + workload)

    def update_workload(self, new_workload: timedelta) -> Task:
        return replace(self, finished_workload=new_workload)

    def delete_child(self, child_id: str) -> Task:
        children = deepcopy(self.children_task_id)
        children.remove(child_id)
        return replace(self, children_task_id=children)

    def add_child(self, child_id: str) -> Task:
        if self.done:
            raise AlreadyDoneParentTaskException()
        children = deepcopy(self.children_task_id)
        children.append(child_id)
        return replace(self, children_task_id=children)

    @classmethod
    def is_root(cls, task_id: str) -> bool:
        return task_id == ROOT_TASK_ID
