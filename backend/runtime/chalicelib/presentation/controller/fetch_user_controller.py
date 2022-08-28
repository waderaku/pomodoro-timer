import json
import traceback
from typing import Optional

from chalice import Response
from chalice.app import Request
from chalicelib.domain.exception.custom_exception import NoExistUserException
from chalicelib.domain.model.value import google_config
from chalicelib.presentation.http.common.user_model import (
    Calender,
    DefaultLength,
    GoogleConfig,
    TaskList,
    UserModel,
)
from chalicelib.usecase.service.fetch_user_service import fetch_user_service


def fetch_user(request: Request) -> Response:
    user_id = request.context["authorizer"]["user_id"]
    try:
        user = fetch_user_service(user_id=user_id)
    except NoExistUserException as e:
        traceback.print_exc()
        return Response(
            status_code=404, body=traceback.format_exception_only(type(e), e)
        )
    body_dict = json.loads(
        UserModel(
            isGoogleLinked=user._is_google_linked,
            googleConfig=create_google_config(user._google_config),
            defaultLength=DefaultLength(
                work=user._default_length.work, rest=user._default_length.rest
            ),
        ).json()
    )
    return Response(body=body_dict)


def create_google_config(
    google_config: google_config.GoogleConfig,
) -> Optional[GoogleConfig]:
    if not google_config:
        return
    return GoogleConfig(
        calendar=Calender(
            id=google_config.calendar.id, name=google_config.calendar.name
        ),
        taskList=TaskList(
            id=google_config.task_list.id, name=google_config.task_list.name
        ),
    )
