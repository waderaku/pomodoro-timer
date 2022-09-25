from abc import ABC, abstractmethod

from chalicelib.domain.model.collection.task_tree import TaskTree
from chalicelib.domain.model.entity.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def fetch_task_tree(self, user_id: str) -> TaskTree:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task: Task):
        raise NotImplementedError

    @abstractmethod
    def register_task(self, task: Task):
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: str):
        raise NotImplementedError
