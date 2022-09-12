import json
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process
from test.db_util import fetch_token

import pytest
from chalicelib.usecase.service.login_service import login_service

test_data_success_path = SERVICE_PATH.joinpath("test_login_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = SERVICE_PATH.joinpath("test_login_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########ログイン正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_login_service_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    token_user = login_service(**request)
    expected_token = fetch_token(token_user._auth_token.value)

    assert token_user._user_id == expected_token["DataValue"]
    assert token_user._auth_token.value == expected_token["DataType"]
    assert token_user._auth_token.deadline.isoformat() == expected_token["Deadline"]


##########ユーザー取得異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_login_service_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        user = login_service(**request)
    assert str(e.value) == answer["error_message"]
