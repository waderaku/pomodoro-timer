import datetime

import pytest
from chalicelib.domain.model.collection.task_tree import TaskTree
from chalicelib.domain.model.entity.task import ROOT_TASK_ID, Task

TEST_TASK_LIST = [
    Task.create_root("1"),
    Task(
        user_id="1",
        task_id="1",
        name="test1",
        shortcut_flg=True,
        children_task_id=["2", "3"],
        parent_id=ROOT_TASK_ID,
        event_id_list=[],
        done=False,
        finished_workload=0,
        estimated_workload=100,
        deadline=datetime.datetime.today(),
        notes="",
    ),
    Task(
        user_id="1",
        task_id="2",
        name="test1",
        shortcut_flg=False,
        children_task_id=[],
        parent_id="1",
        event_id_list=[],
        done=False,
        finished_workload=0,
        estimated_workload=100,
        deadline=datetime.datetime.today(),
        notes="",
    ),
    Task(
        user_id="1",
        task_id="3",
        name="test1",
        shortcut_flg=False,
        children_task_id=["4"],
        parent_id="1",
        event_id_list=[],
        done=False,
        finished_workload=0,
        estimated_workload=100,
        deadline=datetime.datetime.today(),
        notes="",
    ),
    Task(
        user_id="1",
        task_id="4",
        name="test1",
        shortcut_flg=False,
        children_task_id=[],
        parent_id="3",
        event_id_list=[],
        done=False,
        finished_workload=0,
        estimated_workload=100,
        deadline=datetime.datetime.today(),
        notes="",
    ),
]
task_tree = TaskTree(TEST_TASK_LIST)


def test_get_task_scuuess():
    task = task_tree.get_task("4")
    assert task.task_id == "4"


def test_get_task_failed():
    with pytest.raises(Exception) as e:
        task_tree.get_task("5")
    assert str(e.value) == "対象のタスクが存在しません"


def test_get_ancestor_list():
    ancestor_id_list = [task.task_id for task in task_tree._get_ancestor_list("4")]
    ancestor_id_list == ["3", "1"]
