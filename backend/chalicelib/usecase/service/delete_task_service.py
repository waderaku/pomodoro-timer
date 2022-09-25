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
    updated_event_list = _replace_parent(event_list, parent.task_id)

    with repository.batch_writer():
        for desc_id in delete_task_id_list:
            repository.task_repository.delete_task(desc_id)
        repository.task_repository.update_task(updated_parent)
        for event in updated_event_list:
            repository.event_repository.update_event(event)


def _replace_parent(event_list: list[Event], parent_id: str) -> list[Event]:
    return [event.update_task_id(parent_id) for event in event_list]


# TODO
# Comment削除
#     event_list = table.query(KeyConditionExpression=Key("ID").eq(f"{user_id}_event"))[
#         "Items"
#     ]
#     delete_task_list = _get_delete_task(task_list, task_id)

#     update_list = _get_update_data(event_list, task_list, delete_task_list, task_id)
#     with table.batch_writer() as batch:
#         for delete_task in delete_task_list:
#             batch.delete_item(
#                 Key={"ID": delete_task["ID"], "DataType": delete_task["DataType"]}
#             )

#         for update_data in update_list:
#             batch.put_item(Item=update_data)


# def _get_update_data(
#     event_list: list[dict],
#     task_list: list[dict],
#     delete_task_list: list[dict],
#     task_id: str,
# ) -> list[dict]:
#     parent_task = _get_parent_task(task_list, task_id)

#     delete_task_id_list = [delete_task["DataType"] for delete_task in delete_task_list]

#     # タスクが削除された場合親タスクにイベントを全て移動する
#     update_list = [
#         {**event, "DataValue": parent_task["DataType"]}
#         for event in event_list
#         if event["DataValue"] in delete_task_id_list
#     ]

#     parent_task["TaskInfo"]["children_task_id"].remove(task_id)
#     update_list.append(parent_task)
#     return update_list


# def _get_parent_task(task_list: list[dict], task_id: str) -> dict:
#     for task in task_list:
#         if task_id in task["TaskInfo"]["children_task_id"]:
#             return task


# def _get_delete_task(task_list: list[dict], delete_task_id: str) -> list[dict]:
#     task_dict = _create_task_dict(task_list)
#     delete_task_list = []
#     _add_delete_task(task_dict, delete_task_id, delete_task_list)
#     return delete_task_list


# def _add_delete_task(
#     task_dict: dict, delete_task_id: str, delete_task_list: list[dict]
# ):
#     delete_task = task_dict[delete_task_id]
#     delete_task_list.append(delete_task)
#     children_task_id_list = delete_task["TaskInfo"]["children_task_id"]
#     if len(children_task_id_list) == 0:
#         return
#     for child_task in children_task_id_list:
#         _add_delete_task(task_dict, child_task, delete_task_list)


# def _create_task_dict(task_list: list[dict]) -> dict:
#     task_dict = {task["DataType"]: task for task in task_list}
#     return task_dict
