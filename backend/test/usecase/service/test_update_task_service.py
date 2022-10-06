import json
from datetime import datetime
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process
from test.db_util import fetch_task, scan_table

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
def test_update_task_success():
    request, answer = initial_process(test_data_success_list[0])
    request["deadline"] = datetime.fromisoformat(request["deadline"])
    update_task_service(**request)
    updated_table = scan_table()
    assert not DeepDiff(answer, updated_table, ignore_order=True)


@pytest.mark.parametrize("test_data_success", test_data_success_list[1:3])
def test_update_for_children_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)
    request["deadline"] = datetime.fromisoformat(request["deadline"])
    update_task_service(**request)

    expected = list(filter(lambda x: x["ID"] == f"{request['user_id']}_task", answer))
    task_list = fetch_task(request["user_id"])

    assert expected == task_list


def test_update_for_parent_task_success():
    request, answer = initial_process(test_data_success_list[3])
    request["deadline"] = datetime.strptime(request["deadline"], "%Y-%m-%d")
    update_task_service(**request)

    task_list = fetch_task(request["user_id"])

    expected_task_list = list(filter(lambda record: "TaskInfo" in record, answer))
    assert expected_task_list == task_list


##########タスク登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_update_task_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    with pytest.raises(Exception) as e:
        update_task_service(**request)
    assert str(e.value) == answer["error_message"]
