from typing import Callable

from chalice import Chalice

from chalicelib.presentation.controller.authorize_controller import authorize

from .presentation.controller.login_controller import login


def route(app: Chalice, handler: Callable, path: str, methods: list[str]):
    def wrapped(*args, **kwargs):
        return handler(app, *args, **kwargs)

    app.route(path, methods=methods)(wrapped)


def app_routing(app: Chalice):
    app.authorizer()(authorize)
    route(app, login, "/test", ["POST"])
