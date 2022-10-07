import json
from datetime import datetime
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process
from test.db_util import fetch_task

import pytest
from chalicelib.usecase.service.update_task_service import update_task_service
from deepdiff import DeepDiff

test_data_success_path = SERVICE_PATH.joinpath("test_update_task_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = SERVICE_PATH.joinpath("test_update_task_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########タスク更新正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_update_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    request["deadline"] = datetime.fromisoformat(request["deadline"])
    update_task_service(**request)

    expected = list(filter(lambda x: x["ID"] == f"{request['user_id']}_task", answer))
    task_list = fetch_task(request["user_id"])

    assert not DeepDiff(expected, task_list, ignore_order=True)


##########タスク登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_update_task_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        update_task_service(**request)
    assert str(e.value) == answer["error_message"]
