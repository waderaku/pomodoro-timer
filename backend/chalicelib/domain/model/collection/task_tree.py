import itertools
from collections import deque
from datetime import datetime, timedelta
from functools import reduce
from operator import add

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

        updated_estimated_task_list = self._update_ancestor_task(task)

        # 見積もり時間に変更がない場合、親タスクの変更情報だけ返却
        if not updated_estimated_task_list:
            return [update_parent_task]

        return updated_estimated_task_list

    def update_task_tree(self, task: Task) -> list[Task]:
        """対象のタスクを更新し、それによって伝播的に変更となるツリー内のタスク情報を返却する

        Args:
            task (Task): 変更対象のタスク

        Returns:
            list[Task]: 更新したタスク情報一覧
        """
        task_id = task.task_id
        if not self.exists(task_id):
            raise NoExistTaskException()
        self._tree_dict[task_id] = task

        updated_ancestor_list = self._update_ancestor_task(task)

        updated_descendant_task_list = self._update_descendant_task(task, [])

        return list(
            itertools.chain.from_iterable(
                [updated_ancestor_list, updated_descendant_task_list]
            )
        )

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

    def _update_ancestor_task(self, updated_task: Task) -> list[Task]:
        """更新済みのタスクに従い、そのタスクの「祖先」にその変更情報を伝播させる
        伝播させた結果、変更となった他のタスク情報を返却する

        Args:
            updated_task (Task): 更新済みタスク

        Returns:
            list[Task]: 変更となった祖先タスク
        """
        updated = list()

        # それぞれのパラメータの変更が完了していることを示すフラグ
        complete_update_estimated_workload = False
        complete_update_deadline = False
        # タスクが完了済みであれば、変更しない
        complete_update_done = updated_task.done

        while not Task.is_root(updated_task.task_id):
            # 親を取得
            parent = self.get_parent(updated_task.task_id)

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

            # 子タスクがFalseかつ親タスクがTrueの場合に、親タスクをFalseに変更する
            if not complete_update_done:
                if parent.done:
                    parent = parent.resume()
                else:
                    complete_update_done = True

            # 全ての更新が完了したら終了
            if (
                complete_update_estimated_workload
                and complete_update_deadline
                and complete_update_done
            ):
                break

            updated.append(parent)
            updated_task = parent
        return updated

    def _update_descendant_task(
        self,
        updated_task: Task,
        update_descendant_task_list: list[Task],
    ) -> list[Task]:
        """更新済みのタスクに従い、そのタスクの「子孫」にその変更情報を伝播させる
        伝播させた結果、変更となった他のタスク情報を返却する

        Args:
            updated_task (Task): 更新済みタスク
            update_descendant_task_list (Optional[list[Task]]): 更新した子孫タスクの一覧

        Returns:
            list[Task]: 変更となった子孫タスク
        """

        for child_task_id in updated_task.children_task_id:
            child_task = self.get_task(child_task_id)
            # 親タスクが完了済みで子タスクが未完了となっていた場合、子タスクを完了させる
            if updated_task.done and not child_task.done:
                child_task = child_task.finish()
                update_descendant_task_list.append(child_task)
                self._update_descendant_task(child_task, update_descendant_task_list)
        return update_descendant_task_list

    def _get_max_children_deadline(self, task: Task) -> datetime:
        return max(self.get_task(task_id).deadline for task_id in task.children_task_id)

    def get_sum_children_estimated_workload(self, task: Task) -> timedelta:
        return reduce(
            add,
            [
                self.get_task(task_id).estimated_workload
                for task_id in task.children_task_id
            ],
        )

    def add_workload(self, task_id: str, workload: timedelta) -> list[Task]:
        def add_workload(task: Task) -> Task:
            new_task = task.add_workload(workload)
            return new_task

        ancestor_list = self._get_ancestor_list(task_id)
        updated_task_list = [add_workload(ancestor) for ancestor in ancestor_list]
        return updated_task_list
