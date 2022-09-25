from datetime import datetime

import inject
from chalicelib.domain.model.collection.task_tree import TaskTree
from chalicelib.domain.model.entity.event import Event
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.repository import Repository


@inject.params(repository=Repository)
def register_event_service(
    user_id: str,
    task_id: str,
    start: datetime,
    end: datetime,
    repository: Repository,
):
    # TODO
    # Docstring修正
    """対応するタスクのイベント情報の登録及び各タスクの作業完了時間の更新を行う

    Args:
        user_id (str): ユーザID
        task_id (str): タスクID
        start (datetime): 作業開始時間
        end (datetime): 作業終了時間
    """
    task_tree = repository.task_repository.fetch_task_tree(user_id)

    # Event作成
    event = Event.create(user_id, task_id, start, end)
    updated_task_list = _apply_event(task_tree, event)

    with repository.batch_writer():
        repository.event_repository.update_event(event)
        for task in updated_task_list:
            repository.task_repository.update_task(task)


def _apply_event(task_tree: TaskTree, event: Event) -> list[Task]:
    workload = event.end - event.start
    return task_tree.add_workload(event.task_id, workload)
