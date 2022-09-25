from datetime import datetime

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
        estimated_workload=estimated_workload,
        deadline=deadline,
        notes=notes,
        shortcut_flg=shortcut_flg,
    )

    try:
        parent = task_tree.get_parent(task.task_id)
    except NoExistTaskException:
        raise NoExistParentTaskException()

    updated_parent = parent.add_child(task.task_id)
    updated_ancestor_list = task_tree.update_task_estimated_workload(task)

    with repository.batch_writer():
        repository.task_repository.register_task(task)
        repository.task_repository.update_task(updated_parent)
        for ancestor in updated_ancestor_list:
            repository.task_repository.update_task(ancestor)
