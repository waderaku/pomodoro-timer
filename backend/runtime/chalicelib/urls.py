from typing import Callable, Optional

from chalice import Chalice

from chalicelib.presentation.controller.authorize_controller import authorize
from chalicelib.presentation.controller.register_event_controller import register_event

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
    route(app, login, "/login", ["POST"])
    route(app, register_event, "/event", ["POST"], authorizer)
