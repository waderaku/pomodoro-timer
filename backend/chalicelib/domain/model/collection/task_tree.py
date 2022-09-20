from chalicelib.domain.exception.custom_exception import NoExistTaskException
from chalicelib.domain.model.entity.task import ROOT_TASK_ID, Task


class TaskTree:
    def __init__(self, task_list: list[Task]):
        self.tree = {task.task_id: task for task in task_list}

    def get_task(self, task_id: str) -> Task:
        """タスクIDに紐づいたタスクを取得する

        Args:
            task_id (str): タスクID

        Raises:
            NoExistTaskException: 対象のタスクIDに紐づくタスクが存在しないことを示す例外

        Returns:
            Task: 取得したタスク情報
        """
        if task_id in self.tree:
            return self.tree.get(task_id)

        raise NoExistTaskException()

    def get_ancestor_list(self, task_id: str) -> list[Task]:
        """タスクIDに紐づくタスクの親タスク一覧を取得する
        ただし、rootタスクは除く

        Args:
            task_id (str): タスクID

        Returns:
            list[Task]: 親タスク一覧
        """
        task = self.get_task(task_id)
        ancestor_list = []
        while task.parent_id != ROOT_TASK_ID:
            task = self.get_task(task.parent_id)
            ancestor_list.append(task)

        return ancestor_list
