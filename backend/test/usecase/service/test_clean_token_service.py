import json
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process
from test.db_util import fetch_token_list

import pytest
from chalicelib.usecase.service.clean_token_service import clean_token_service

test_data_success_path = SERVICE_PATH.joinpath("test_clean_token_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


##########トークンクリーン正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_clean_token_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    clean_token_service()
    token_list = fetch_token_list()
    assert token_list == answer
