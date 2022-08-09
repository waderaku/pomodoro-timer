from chalice import Chalice
from runtime.chalicelib.presentation.controller.authorize_controller import \
    authorize


def app_routing(app: Chalice):
    app.authorizer()(authorize)
