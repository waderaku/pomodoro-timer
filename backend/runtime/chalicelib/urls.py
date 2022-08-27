from typing import Callable, Optional

from chalice import Chalice, Rate

from chalicelib.presentation.controller.authorize_controller import authorize
from chalicelib.presentation.controller.clean_token_controller import crean_token
from chalicelib.presentation.controller.fetch_user_controller import fetch_user
from chalicelib.presentation.controller.register_event_controller import register_event
from chalicelib.presentation.controller.register_user_controller import register_user
from chalicelib.presentation.controller.update_user_controller import update_user

from .presentation.controller.login_controller import login


def route(
    app: Chalice,
    handler: Callable,
    path: str,
    methods: list[str],
    authorizer: Optional[Callable] = None,
):
    def wrapped(*args, **kwargs):
        return handler(app.current_request, *args, **kwargs)

    app.route(path, methods=methods, authorizer=authorizer)(wrapped)


def app_routing(app: Chalice):
    authorizer = app.authorizer()(authorize)
    app.schedule(Rate(3, unit=Rate.DAYS))(crean_token)
    route(app, login, "/login", ["POST"])
    route(app, register_event, "/event", ["POST"], authorizer)
    route(app, fetch_user, "/user", ["GET"], authorizer)
    route(app, update_user, "/user", ["PUT"], authorizer)
    route(app, register_user, "/user", ["POST"])
