from chalicelib.domain.exception.custom_exception import NoExistUserException
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.repository import Repository


def fetch_task_service(user_id: str, repository: Repository) -> list[Task]:
    # TODO Docstring
    task_tree = repository.task_repository.fetch_task_tree(user_id)

    # タスクが存在しない場合ユーザ登録が完了していない
    if task_tree.is_empty():
        raise NoExistUserException()

    return task_tree.as_task_list()
