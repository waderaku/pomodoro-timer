from chalicelib.domain.model.collection.task_tree import TaskTree
from boto3.dynamodb.conditions import Key
from chalicelib.domain.model.entity.task import Task
from chalicelib.domain.repository.task_repository import TaskRepository
from chalicelib.infrastructure.dynamodb.model.task_model import TaskDynamoModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import (
    DynamoRepository,
)


class TaskDynamoRepository(TaskRepository, DynamoRepository):
    def fetch_task_tree(self, user_id: str) -> TaskTree:
        task_dynamo_items: list[dict] = self._table.query(
            KeyConditionExpression=Key("ID").eq(f"{user_id}_task")
        )["Items"]
        task_list = [TaskDynamoModel(**item).to_task() for item in task_dynamo_items]
        tree_dict = {task.task_id: task for task in task_list}
        return TaskTree(tree_dict)

    def batch_update_task(self, task_list: list[Task]):
        dynamo_model_list = [TaskDynamoModel.from_task(task) for task in task_list]
        with self._table.batch_writer() as batch:
            self.batch_update(dynamo_model_list)
            # for dynamo_model in dynamo_model_list:
            #     batch.put_item(Item=dynamo_model.to_dynamo_input())
