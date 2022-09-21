from abc import ABC, abstractmethod

from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.model.value.task_tree import TaskTree


class TaskRepository(ABC):
    @abstractmethod
    def fetch_task_tree(self, user_id: str) -> TaskTree:
        raise NotImplementedError

    @abstractmethod
    def batch_update_task(self, task_list: list[Task]):
        raise NotImplementedError
