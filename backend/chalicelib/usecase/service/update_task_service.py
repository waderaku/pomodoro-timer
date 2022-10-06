from datetime import datetime, timedelta

import inject
from chalicelib.domain.exception.custom_exception import (
    NoExistUserException,
    UpdateRootTaskException,
)
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.repository import Repository

table_name = "pomodoro_info"


@inject.params(repository=Repository)
def update_task_service(
    user_id: str,
    task_id: str,
    name: str,
    estimated_workload: int,
    deadline: datetime,
    notes: str,
    done: bool,
    shortcut_flg: bool,
    repository: Repository,
):
    task_tree = repository.task_repository.fetch_task_tree(user_id)
    if task_tree.is_empty():
        raise NoExistUserException()

    task = task_tree.get_task(task_id)
    if Task.is_root(task.task_id):
        raise UpdateRootTaskException()

    updated_task = task.update_task_base_info(
        name, timedelta(seconds=estimated_workload), deadline, notes, done, shortcut_flg
    )

    updated_related_task_list = task_tree.update_task_tree(updated_task)

    with repository.batch_writer():
        repository.task_repository.update_task(updated_task)
        for updated_related_task in updated_related_task_list:
            repository.task_repository.update_task(updated_related_task)
    return updated_task
