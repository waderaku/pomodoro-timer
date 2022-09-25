import traceback
from chalice import Response
from chalice.app import Request
from chalicelib.domain.exception.custom_exception import (DeleteRootTaskException,
                                                          NoExistTaskException,
                                                          NoExistUserException)
from chalicelib.usecase.service.delete_task_service import delete_task_service


def delete_task(request: Request, id: str):
    user_id = request.context["authorizer"]["user_id"]

    try:
        delete_task_service(user_id=user_id, task_id=id)
    except (NoExistTaskException, NoExistUserException) as e:
        traceback.print_exc()
        return Response(
            status_code=404, body=traceback.format_exception_only(type(e), e)
        )
    except DeleteRootTaskException as e:
        traceback.print_exc()
        return Response(
            status_code=400, body=traceback.format_exception_only(type(e), e)
        )
