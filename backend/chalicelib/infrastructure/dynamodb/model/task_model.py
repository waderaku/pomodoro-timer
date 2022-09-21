from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import ROUND_HALF_UP, Decimal

from chalicelib.domain.model.entity.task import Task


@dataclass
class TaskInfoDynamoModel:
    name: str
    shortcut_flg: bool
    parent_id: str
    children_task_id: list[str]
    finished_workload: int
    estimated_workload: int
    deadline: str
    notes: str

    def __post_init__(self):
        self.finished_workload = self._quantize(self.finished_workload)
        self.estimated_workload = self._quantize(self.estimated_workload)

    def _quantize(self, float_variable: float) -> float:
        return float(
            Decimal(str(float_variable)).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )
        )


@dataclass
class TaskDynamoModel:
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

    # TODO CDKでTable定義にparentId加える

    def to_task(self) -> Task:
        return Task(
            user_id=self.ID.split("_")[0],
            task_id=self.DataType,
            parent_id=self.TaskInfo.parent_id,
            name=self.TaskInfo.name,
            shortcut_flg=self.TaskInfo.shortcut_flg,
            children_task_id=self.TaskInfo.children_task_id,
            finished_workload=self.TaskInfo.finished_workload,
            estimated_workload=self.TaskInfo.estimated_workload,
            deadline=self.TaskInfo.deadline,
        )

    def to_dynamo_input(self) -> dict:
        return asdict(self)
