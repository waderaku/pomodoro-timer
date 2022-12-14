import json
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process

import pytest
from chalicelib.usecase.service.authorize_service import authorize_service

test_data_success_path = SERVICE_PATH.joinpath("test_authorize_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = SERVICE_PATH.joinpath("test_authorize_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########トークン認証正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_authorize_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    token_user = authorize_service(**request)
    assert token_user._user_id == answer["user_id"]
    assert token_user._auth_token.value == answer["auth_token"]["value"]
    assert (
        token_user._auth_token.deadline.isoformat() == answer["auth_token"]["deadline"]
    )


##########トークン認証異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_authorize_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        authorize_service(**request)
    assert str(e.value) == answer["error_message"]
