import traceback
from typing import Optional

from chalice import Response
from chalice.app import Request
from src.domain.exception.custom_exception import (
    AdditionalNegativeValueException,
    NoExistTaskException,
)
from src.usecase.service.register_event_service import register_event_service


def register_event(request: Request) -> Optional[Response]:
    body = request.json_body
    user_id = request.context["authorizer"]["user_id"]
    try:
        register_event_service(
            user_id, task_id=body["taskId"], start=body["start"], end=body["end"]
        )
    except NoExistTaskException as e:
        traceback.print_exc()
        return Response(
            status_code=404, body=traceback.format_exception_only(type(e), e)
        )
    except AdditionalNegativeValueException as e:
        traceback.print_exc()
        return Response(
            status_code=400, body=traceback.format_exception_only(type(e), e)
        )
