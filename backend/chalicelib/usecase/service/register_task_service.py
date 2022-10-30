from datetime import datetime, timedelta

import inject
from chalicelib.domain.exception.custom_exception import (
    NoExistParentTaskException,
    NoExistTaskException,
    NoExistUserException,
)
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.repository import Repository


@inject.params(repository=Repository)
def register_task_service(
    user_id: str,
    parent_id: str,
    name: str,
    estimated_workload: int,
    deadline: datetime,
    notes: str,
    shortcut_flg: bool,
    repository: Repository,
):
    """新タスクを生成する。
    1. タスクオブジェクトを作成する
    2. 親タスクの子タスクリストに新規タスクのtask_idを追加する
    3. 祖先タスクのestimated_workloadを更新する
    """

    task_tree = repository.task_repository.fetch_task_tree(user_id)
    if task_tree.is_empty():
        raise NoExistUserException()

    task = Task.create(
        user_id=user_id,
        parent_id=parent_id,
        name=name,
        estimated_workload=timedelta(seconds=estimated_workload),
        deadline=deadline,
        notes=notes,
        shortcut_flg=shortcut_flg,
    )
    try:
        updated_task_list = task_tree.add_task(task)
    except NoExistTaskException:
        raise NoExistParentTaskException()

    with repository.batch_writer():
        repository.task_repository.register_task(task)
        for updated_task in updated_task_list:
            repository.task_repository.update_task(updated_task)
    return task
