from collections import deque
from datetime import timedelta

from chalicelib.domain.exception.custom_exception import NoExistTaskException
from chalicelib.domain.model.entity.task import Task


class TaskTree:
    def __init__(self, tree_dict: dict[str, Task]):
        self._tree_dict = tree_dict

    def get_task(self, task_id: str) -> Task:
        """タスクIDに紐づいたタスクを取得する

        Args:
            task_id (str): タスクID

        Raises:
            NoExistTaskException: 対象のタスクIDに紐づくタスクが存在しないことを示す例外

        Returns:
            Task: 取得したタスク情報
        """
        if task_id not in self._tree_dict:
            raise NoExistTaskException()
        return self._tree_dict[task_id]

    def _get_ancestor_list(self, task_id: str) -> list[Task]:
        """タスクIDに紐づくタスク「と」その親タスク一覧を取得する。
        ルートも含む。

        Args:
            task_id (str): タスクID

        Returns:
            list[Task]: 親タスク一覧
        """
        task = self.get_task(task_id)
        ancestor_list = [task]
        while not Task.is_root(task.task_id):
            task = self.get_task(task.parent_id)
            ancestor_list.append(task)
        return ancestor_list

    def get_descendant_id_list(self, task_id: str) -> list[str]:
        # 子孫のリスト
        descendant_list = list()
        # 幅優先探索のFIFO-Queue
        id_list = deque([task_id])

        while len(id_list) > 0:
            # 現在のタスクを取得
            task_id = id_list.popleft()
            descendant_list.append(task_id)

            # 子タスクリストをqueueに追加
            task = self.get_task(task_id)
            id_list.extend(task.children_task_id)
        return descendant_list

    def is_empty(self) -> bool:
        return len(self._tree_dict) == 0

    def exists(self, task_id: str) -> bool:
        return task_id in self._tree_dict

    def as_task_list(self) -> list[Task]:
        return list(self._tree_dict.values())

    def get_parent(self, task_id: str) -> Task:
        return self.get_task(self.get_task(task_id).parent_id)

    def update_task_estimated_workload(self, task: Task) -> list[Task]:
        updated = list()
        while not Task.is_root(task.task_id):
            # 親を取得
            parent = self.get_parent(task.task_id)

            # 親のworkloadより子の合計workloadが大きければ大きい方に更新する
            estimated_workload = self.get_sum_children_estimated_workload(parent)
            if estimated_workload > parent.estimated_workload:
                self._tree_dict[parent.task_id] = parent.update_workload(
                    estimated_workload
                )
                updated.append(parent)
            task = parent
        return updated

    def get_sum_children_estimated_workload(self, task: Task) -> float:
        return sum(
            self.get_task(task_id).estimated_workload
            for task_id in task.children_task_id
        )

    def add_workload(self, task_id: str, workload: timedelta) -> list[Task]:
        def add_workload(task: Task) -> Task:
            new_task = task.add_workload(workload)
            return new_task

        ancestor_list = self._get_ancestor_list(task_id)
        updated_task_list = [add_workload(ancestor) for ancestor in ancestor_list]
        return updated_task_list
