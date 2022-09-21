from datetime import datetime, timedelta

import inject
from chalicelib.domain.model.entity.event import Event
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.model.value.task_tree import TaskTree
from chalicelib.domain.repository.event_repository import EventRepository
from chalicelib.domain.repository.task_repository import TaskRepository


@inject.params(task_tree_repository=TaskRepository)
@inject.params(event_repository=EventRepository)
def register_event_service(
    user_id: str,
    task_id: str,
    start: datetime,
    end: datetime,
    task_repository: TaskRepository,
    event_repository: EventRepository,
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
    task_tree = task_repository.fetch_task_tree(user_id)
    # イベントが追加されるタスクとその祖先の取得
    ancestor_list = _get_ancestor_list(task_id, task_tree)

    # 作業時間
    workload = end - start
    # Event作成
    event = Event.create(task_id, start, end)
    # 作業時間の計上
    _add_workload(ancestor_list, workload, task_repository)
    # イベントの登録
    event_repository.register_event(event)


def _get_ancestor_list(task_id: str, task_tree: TaskTree) -> list[Task]:
    task = task_tree.get_task(task_id)
    ancestor_list = [task]
    while not task.is_root():
        task = task_tree.get_task(task.parent_id)
        ancestor_list.append(task)
    return ancestor_list


def _add_workload(
    ancestor_list: list[Task], workload: timedelta, task_repository: TaskRepository
):
    def add_workload(task: Task) -> Task:
        new_task = task.update(finished_workload=task.finished_workload + workload)
        return new_task

    updated_task_list = [add_workload(ancestor) for ancestor in ancestor_list]
    task_repository.batch_update_task(updated_task_list)
