from collections import deque
from datetime import datetime, timedelta

from chalicelib.domain.exception.custom_exception import NoExistTaskException
from chalicelib.domain.model.entity.task import Task


class TaskTree:
    def __init__(self, tree_dict: dict[str, Task]):
        self._tree_dict = tree_dict

    def add_task(self, task: Task) -> list[Task]:
        """タスクを追加し、それによって更新したツリー内のタスク情報を返却する

        Args:
            task (Task): 追加するタスク

        Returns:
            list[Task]: 更新したタスク情報一覧
        """
        task_id = task.task_id

        # ツリーにタスクの追加
        self._tree_dict[task_id] = task

        # 親タスクに当該タスク情報を追加
        parent_task = self.get_parent(task_id)
        update_parent_task = parent_task.add_child(task_id)
        self._tree_dict[parent_task.task_id] = update_parent_task

        # タスクに入れた見積もり情報に応じて祖先タスクの見積もり情報及び期日を更新
        updated_estimated_task_list = self._update_task_estimated_workload_and_deadline(
            task
        )

        # 見積もり時間に変更がない場合、親タスクの変更情報だけ返却
        if not updated_estimated_task_list:
            return [update_parent_task]

        return updated_estimated_task_list

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

    def _update_task_estimated_workload_and_deadline(self, task: Task) -> list[Task]:
        updated = list()

        # それぞれのフラグがTrueの時に更新が行われる
        complete_update_estimated_workload = False
        complete_update_deadline = False

        while not Task.is_root(task.task_id):
            # 親を取得
            parent = self.get_parent(task.task_id)

            # 親のworkloadより子の合計workloadが大きければ大きい方に更新する
            if not complete_update_estimated_workload:
                estimated_workload = self.get_sum_children_estimated_workload(parent)
                if estimated_workload > parent.estimated_workload:
                    parent = parent.update_estimated_workload(estimated_workload)
                    self._tree_dict[parent.task_id] = parent
                else:
                    complete_update_estimated_workload = True

            # 親のdeadlineと子のdeadlineの中で最も後の日付を比較し、親の方が前の日付の場合更新する
            if not complete_update_deadline:
                children_deadline = self._get_max_children_deadline(parent)
                if children_deadline > parent.deadline:
                    parent = parent.update_deadline(children_deadline)
                    self._tree_dict[parent.task_id] = parent
                else:
                    complete_update_deadline = True

            # 両方の更新が完了したら終了
            if complete_update_estimated_workload and complete_update_deadline:
                break

            updated.append(parent)
            task = parent
        return updated

    def _get_max_children_deadline(self, task: Task) -> datetime:
        return max(self.get_task(task_id).deadline for task_id in task.children_task_id)

    def get_sum_children_estimated_workload(self, task: Task) -> timedelta:
        return timedelta(
            seconds=sum(
                self.get_task(task_id).estimated_workload.total_seconds()
                for task_id in task.children_task_id
            )
        )

    def add_workload(self, task_id: str, workload: timedelta) -> list[Task]:
        def add_workload(task: Task) -> Task:
            new_task = task.add_workload(workload)
            return new_task

        ancestor_list = self._get_ancestor_list(task_id)
        updated_task_list = [add_workload(ancestor) for ancestor in ancestor_list]
        return updated_task_list
