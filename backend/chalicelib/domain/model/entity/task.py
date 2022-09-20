from __future__ import annotations

from datetime import datetime

ROOT_TASK_ID = "root"
ROOT_TASK_NAME = "HOME"
ROOT_TASK_WORKLOAD = 105120000


class Task:
    """タスクドメイン"""

    def __init__(
        self,
        user_id: str,
        task_id: str,
        name: str,
        shortcut_flg: bool,
        children_task_id: list[str],
        parent_id: str,
        event_id_list: list[str],
        done: bool,
        finished_workload: int,
        estimated_workload: int,
        deadline: datetime,
        notes: str,
    ):
        self._user_id = user_id
        self._task_id = task_id
        self._name = name
        self._shortcut_flg = shortcut_flg
        self._children_task_id = children_task_id
        self._parent_id = parent_id
        self._event_id_list = event_id_list
        self._done = done
        self._finished_workload = finished_workload
        self._estimated_workload = estimated_workload
        self._deadline = deadline
        self._notes = notes

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def shortcut_flg(self) -> bool:
        return self._shortcut_flg

    @property
    def children_task_id(self) -> list[str]:
        return self._children_task_id

    @property
    def parent_id(self) -> str:
        return self._parent_id

    @property
    def event_id_list(self) -> list[str]:
        return self._event_id_list

    @property
    def done(self) -> bool:
        return self._done

    @property
    def finished_workload(self) -> int:
        return self._finished_workload

    @property
    def estimated_workload(self) -> int:
        return self._estimated_workload

    @property
    def deadline(self) -> datetime:
        return self._deadline

    @property
    def notes(self) -> str:
        return self._notes

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
            parent_id="",
            _event_id_list=[],
            finished_workload=ROOT_TASK_WORKLOAD,
            estimated_workload=ROOT_TASK_WORKLOAD,
            deadline="2200-12-31",
            notes="",
        )
