from chalicelib.domain.exception.custom_exception import NoExistTaskException
from chalicelib.domain.model.entity.task import Task


class TaskTree:
    def __init__(self, tree_dict: dict[str, Task]):
        self._tree_dict = tree_dict

    def get_task(self, task_id: str) -> Task:
        if task_id not in self._tree_dict:
            raise NoExistTaskException()
        return self._tree_dict[task_id]
