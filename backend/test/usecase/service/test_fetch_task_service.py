import json
from dataclasses import asdict
from datetime import datetime, timedelta
from decimal import Decimal
from test.common import SERVICE_PATH, initial_process

import pytest
from chalicelib.usecase.service.fetch_task_service import fetch_task_service
from deepdiff import DeepDiff

test_data_success_path = SERVICE_PATH.joinpath("test_fetch_task_service_success.json")
with test_data_success_path.open("r") as f:
    test_data_success_list: list = json.load(f, parse_float=Decimal)


test_data_failed_path = SERVICE_PATH.joinpath("test_fetch_task_service_failed.json")
with test_data_failed_path.open("r") as f:
    test_data_failed_list: list = json.load(f, parse_float=Decimal)


def convert_to_correct_type(data_list: list[dict]):
    [
        data.update(
            {
                "finished_workload": timedelta(
                    seconds=float(data["finished_workload"])
                ),
                "estimated_workload": timedelta(
                    seconds=float(data["estimated_workload"])
                ),
                "deadline": datetime.fromisoformat(data["deadline"]),
            }
        )
        for data in data_list
    ]


##########タスク取得正常系テスト##############
@pytest.mark.parametrize("test_data_success", test_data_success_list)
def test_fetch_task_success(test_data_success: dict):
    request, answer = initial_process(test_data_success)

    # answerの時間をtimedeltaに,deadlineをdatetime変換
    convert_to_correct_type(answer)

    task_list = fetch_task_service(**request)
    assert not DeepDiff(answer, [asdict(task) for task in task_list], ignore_order=True)


##########タスク取得異常系テスト##############
@pytest.mark.parametrize("test_data_failed", test_data_failed_list)
def test_fetch_task_failed(test_data_failed: dict):
    request, answer = initial_process(test_data_failed)

    with pytest.raises(Exception) as e:
        fetch_task_service(**request)
    assert str(e.value) == answer["error_message"]
