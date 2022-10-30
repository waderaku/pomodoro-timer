import json
from datetime import datetime
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process
from test.db_util import fetch_task, fetch_task_by_task_id

import pytest
from chalicelib.usecase.service.register_task_service import register_task_service
from deepdiff import DeepDiff

test_data_success_path = SERVICE_PATH.joinpath(
    "test_register_task_service_success.json"
)
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = SERVICE_PATH.joinpath("test_register_task_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)

##########タスク登録正常系テスト##############
#######①root直下タスクの登録ができることのテスト#########


def test_parent_register_task():
    request, answer = initial_process(test_data_success_list[0])
    request["deadline"] = datetime.fromisoformat(request["deadline"])
    task_id = register_task_service(**request).task_id

    task = fetch_task_by_task_id(request["user_id"], task_id)
    task.pop("DataType")
    assert answer == task


#######②root直下以外のタスク登録ができることのテスト（rootタスクの更新はなし）#########
def test_child_register_task_1():
    request, answer = initial_process(test_data_success_list[1])
    request["deadline"] = datetime.fromisoformat(request["deadline"])
    task_id = register_task_service(**request).task_id

    parent_task = fetch_task_by_task_id(request["user_id"], request["parent_id"])
    child_task = fetch_task_by_task_id(request["user_id"], task_id)
    answer["parent_task"]["TaskInfo"]["children_task_id"] = [task_id]
    child_task.pop("DataType")
    assert answer["parent_task"] == parent_task
    assert answer["child_task"] == child_task


#######③oot直下以外のタスク登録ができることのテスト（rootタスクの更新あり・更新が不要になるまで再帰的に更新）#########
def test_child_register_task_2():
    request, answer = initial_process(test_data_success_list[2])
    request["deadline"] = datetime.fromisoformat(request["deadline"])
    task_id = register_task_service(**request).task_id

    user_id = request["user_id"]
    task_list = fetch_task(user_id)

    answer[-1]["DataType"] = task_id

    # 親タスクの子タスク情報に今回作成したタスクIDを追加する
    answer[2]["TaskInfo"]["children_task_id"] = [task_id]

    assert not DeepDiff(answer, task_list, ignore_order=True)


##########タスク登録異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_register_task_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)
    request["deadline"] = datetime.strptime(request["deadline"], "%Y-%m-%d")
    with pytest.raises(Exception) as e:
        register_task_service(**request)
    assert str(e.value) == answer["error_message"]
