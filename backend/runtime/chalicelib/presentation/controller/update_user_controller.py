import traceback
from typing import Optional

from chalice import Response
from chalice.app import Request
from chalicelib.domain.exception.custom_exception import (
    NoExistUserException,
    NotSettingConfigException,
)
from chalicelib.presentation.http.common.user_model import GoogleConfig, UserModel
from chalicelib.usecase.service.update_user_service import update_user_service


def update_user(request: Request) -> Optional[Response]:
    user_id = request.context["authorizer"]
    body = UserModel(**request.json_body)
    default_length = {
        "work": body.defaultLength.work,
        "rest": body.defaultLength.rest,
    }
    try:
        update_user_service(
            user_id=user_id,
            is_google_linked=body.isGoogleLinked,
            default_length=default_length,
            google_config=_create_google_config(body.googleConfig),
        )
    except NoExistUserException as e:
        traceback.print_exc()
        return Response(
            status_code=404, body=traceback.format_exception_only(type(e), e)
        )
    except NotSettingConfigException as e:
        traceback.print_exc()
        return Response(
            status_code=400, body=traceback.format_exception_only(type(e), e)
        )


def _create_google_config(google_config: Optional[GoogleConfig]) -> Optional[dict]:
    if not google_config:
        return
    return {
        "calendar": {
            "id": google_config.calendar.id,
            "name": google_config.calendar.name,
        },
        "task_list": {
            "id": google_config.taskList.id,
            "name": google_config.taskList.name,
        },
    }
