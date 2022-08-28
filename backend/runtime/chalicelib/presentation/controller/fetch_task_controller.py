import json
from chalice import Response
from chalice.app import Request
from chalicelib.presentation.http.response.task_response import (
    TaskData,
    TaskModel,
    TaskResponse,
)
from chalicelib.usecase.service.fetch_task_service import Task, fetch_task_service


table_name = "pomodoro_info"


def fetch_task(request: Request) -> Response:
    user_id = request.context["authorizer"]["user_id"]

    task_list = fetch_task_service(user_id=user_id)
    response_task_list = _create_response_task_list(task_list)
    shortcut_id_list = [task.task_id for task in task_list if task.shortcut_flg]

    body_dict = json.loads(
        TaskResponse(
            task=response_task_list, 
            shortcutTaskId=shortcut_id_list
        ).json()
    )
    return Response(body=body_dict)


def _create_response_task_list(task_list: list[Task]):
    # 親タスクIDを作成
    parent_task_dict = {}
    for task in task_list:
        parent_task_dict.update(
            {child_task: task.task_id for child_task in task.children_task_id}
        )

    return [
        _create_task(task, parent_task_dict.get(task.task_id, "")) for task in task_list
    ]


def _create_task(task: Task, parent_task_id: str):
    task_data = TaskData(
        name=task.name,
        childrenIdList=task.children_task_id,
        parentId=parent_task_id,
        done=task.done,
        finishedWorkload=task.finished_workload,
        estimatedWorkload=task.estimated_workload,
        deadline=task.deadline,
        notes=task.notes,
    )
    return TaskModel(id=task.task_id, taskData=task_data)
