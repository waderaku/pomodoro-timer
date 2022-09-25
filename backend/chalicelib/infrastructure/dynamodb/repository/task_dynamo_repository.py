from boto3.dynamodb.conditions import Key
from chalicelib.domain.model.collection.task_tree import TaskTree
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.task_repository import TaskRepository
from chalicelib.infrastructure.dynamodb.model.task_model import TaskDynamoModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_key import DynamoKey
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import DynamoIO


class TaskDynamoRepository(TaskRepository):
    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def fetch_task_tree(self, user_id: str) -> TaskTree:
        task_dynamo_list = self._dynamo_io.query(
            Key("ID").eq(f"{user_id}_task"), TaskDynamoModel
        )
        task_list = [task_model.to_task() for task_model in task_dynamo_list]
        tree_dict = {task.task_id: task for task in task_list}
        return TaskTree(tree_dict)

    def _upsert_task(self, task: Task):
        task_model = TaskDynamoModel.from_task(task)
        self._dynamo_io.put_item(task_model)

    def update_task(self, task: Task):
        self._upsert_task(task)

    def register_task(self, task: Task):
        self._upsert_task(task)

    def delete_task(self, user_id: str, task_id: str):
        key = DynamoKey(ID=f"{user_id}_task", DataType=task_id)
        self._dynamo_io.delete_item(key)
