import inject
from chalicelib.domain.exception.custom_exception import (
    DeleteRootTaskException,
    NoExistTaskException,
    NoExistUserException,
)
from chalicelib.domain.model.entity.event import Event
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.repository import Repository


@inject.params(repository=Repository)
def delete_task_service(user_id: str, task_id: str, repository: Repository):
    """タスクを削除する。
    1. タスク本体とその子孫のタスクを削除する
    2. 親タスクの子タスクリストから削除されるタスクのidを削除する
    3. 削除タスクに紐付いていたイベントを親のタスクに紐付ける
    """

    if Task.is_root(task_id):
        raise DeleteRootTaskException()

    task_tree = repository.task_repository.fetch_task_tree(user_id)
    if task_tree.is_empty():
        raise NoExistUserException()

    if not task_tree.exists(task_id):
        raise NoExistTaskException()

    # 親タスクの子タスクリストから削除されるタスクのidを削除する
    parent = task_tree.get_parent(task_id)
    # 削除対象の子孫タスクを取得
    delete_task_id_list = task_tree.get_descendant_id_list(task_id)
    # イベントの所属するタスクを削除対象のタスクの親に差し替え
    updated_parent = parent.delete_child(task_id)
    event_list = repository.event_repository.fetch_by_user_id(user_id)
    updated_event_list = _replace_event_task_id(
        event_list, parent.task_id, delete_task_id_list
    )

    with repository.batch_writer():
        for desc_id in delete_task_id_list:
            repository.task_repository.delete_task(user_id, desc_id)
        repository.task_repository.update_task(updated_parent)
        for event in updated_event_list:
            repository.event_repository.update_event(event)


def _replace_event_task_id(
    event_list: list[Event], update_task_id: str, target_task_id_list: list[str]
) -> list[Event]:
    """対象となるタスクIDに紐づくeventのタスクIDを変更する

    Args:
        event_list (list[Event]): 変更対象のイベント一覧
        update_task_id (str): 変更するタスクID
        target_task_id_list (list[str]): 変更の対象となるタスクID

    Returns:
        list[Event]: 変更したイベント一覧
    """
    return [
        event.update_task_id(update_task_id)
        for event in event_list
        if event.task_id in target_task_id_list
    ]
