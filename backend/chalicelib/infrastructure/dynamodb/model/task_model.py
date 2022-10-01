from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import timedelta
from decimal import Decimal

from chalicelib.domain.model.entity.task import Task
from chalicelib.infrastructure.dynamodb.model.dynamo_model import DynamoModel


@dataclass
class TaskInfoDynamoModel:
    name: str
    shortcut_flg: bool
    parent_id: str
    children_task_id: list[str]
    finished_workload: Decimal
    estimated_workload: Decimal
    deadline: str
    notes: str


@dataclass
class TaskDynamoModel(DynamoModel):
    ID: str
    DataType: str
    DataValue: str
    TaskInfo: TaskInfoDynamoModel

    @classmethod
    def from_task(cls, task: Task) -> TaskDynamoModel:
        """ドメインのユーザオブジェクトをDBに登録する形式に変換する

        Args:
            task (Task): ユーザオブジェクト
        """
        task_info_model = TaskInfoDynamoModel(
            name=task.name,
            parent_id=task.parent_id,
            shortcut_flg=task.shortcut_flg,
            children_task_id=task.children_task_id,
            finished_workload=task.finished_workload,
            estimated_workload=task.estimated_workload,
            deadline=task.deadline,
            notes=task.notes,
        )
        return cls(
            ID=f"{task.user_id}_task",
            DataType=task.task_id,
            DataValue="True" if task.done else "False",
            TaskInfo=task_info_model,
        )

    def to_task(self) -> Task:
        return Task(
            user_id=self.ID.split("_")[0],
            task_id=self.DataType,
            name=self.TaskInfo.name,
            shortcut_flg=self.TaskInfo.shortcut_flg,
            children_task_id=self.TaskInfo.children_task_id,
            parent_id=self.TaskInfo.parent_id,
            done=self.DataValue == "True",
            finished_workload=timedelta(seconds=float(self.TaskInfo.finished_workload)),
            estimated_workload=timedelta(
                seconds=float(self.TaskInfo.estimated_workload)
            ),
            deadline=self.TaskInfo.deadline,
            notes=self.TaskInfo.notes,
        )

    def to_dynamo_input(self) -> dict:
        return asdict(self)
