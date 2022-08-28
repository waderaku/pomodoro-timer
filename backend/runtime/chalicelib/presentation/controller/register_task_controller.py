import traceback
from chalice import Response
from chalice.app import Request
from chalicelib.domain.exception.custom_exception import (
    AlreadyDoneParentTaskException,
    NoExistParentTaskException,
    NoExistUserException,
    NotShortcutTaskException,
)
from chalicelib.presentation.http.request.register_task_request import RegisterTaskRequest
from chalicelib.usecase.service.register_task_service import register_task_service


def register_task(request: Request):
    body = RegisterTaskRequest(**request.json_body)
    user_id = request.context["authorizer"]

    try:
        task = register_task_service(
            user_id=user_id,
            parent_id=body.parentId,
            name=body.name,
            estimated_workload=body.estimatedWorkload,
            deadline=body.deadline,
            notes=body.notes,
            shortcut_flg=body.shortcutFlg,
        )
    except (NoExistUserException, NoExistParentTaskException) as e:
        traceback.print_exc()
        return Response(
            status_code=404, body=traceback.format_exception_only(type(e), e)
        )
    except (AlreadyDoneParentTaskException, NotShortcutTaskException) as e:
        traceback.print_exc()
        return Response(
            status_code=400, body=traceback.format_exception_only(type(e), e)
        )
