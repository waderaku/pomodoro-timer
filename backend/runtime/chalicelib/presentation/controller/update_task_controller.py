import traceback

from chalice import Response
from chalice.app import Request
from chalicelib.domain.exception.custom_exception import NoExistTaskException
from chalicelib.presentation.http.request.update_task_request import UpdateTaskRequest
from chalicelib.usecase.service.update_task_service import update_task_service


def update_task(id: str, request: Request):
    body = UpdateTaskRequest(**request.json_body)
    user_id = request.context["authorizer"]

    try:
        update_task_service(
            user_id,
            id,
            body.name,
            body.estimatedWorkload,
            body.deadline,
            body.notes,
            body.done,
            body.shortcutFlg,
        )
    except NoExistTaskException as e:
        traceback.print_exc()
        return Response(
            status_code=404, body=traceback.format_exception_only(type(e), e)
        )
