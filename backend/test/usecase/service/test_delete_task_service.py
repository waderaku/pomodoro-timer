import json
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process
from test.db_util import fetch_event, fetch_task

import pytest
from chalicelib.usecase.service.delete_task_service import delete_task_service
from deepdiff import DeepDiff

test_data_success_path = SERVICE_PATH.joinpath("test_delete_task_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = SERVICE_PATH.joinpath("test_delete_task_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########タスク削除正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_delete_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    delete_task_service(**request)
    task_list = fetch_task(request["user_id"])
    event_list = fetch_event(request["user_id"])
    task_list.extend(event_list)
    assert not DeepDiff(answer, task_list, ignore_order=True)


##########タスク削除異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_delete_task_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        delete_task_service(**request)
    assert str(e.value) == answer["error_message"]
