from typing import Callable, Optional

from chalice import Chalice

from src.presentation.chalice.authorize_controller import authorize
from src.presentation.chalice.fetch_user_controller import fetch_user
from src.presentation.chalice.register_event_controller import register_event
from src.presentation.chalice.register_user_controller import register_user
from src.presentation.chalice.update_user_controller import update_user

from .presentation.chalice.login_controller import login


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
    route(app, fetch_user, "/user", ["GET"], authorizer)
    route(app, update_user, "/user", ["PUT"], authorizer)
    route(app, register_user, "/user", ["POST"])
