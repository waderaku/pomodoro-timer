from chalicelib.domain.model.entity.task_user import TaskUser
from chalicelib.domain.repository.task_user_repository import TaskUserRepository
from chalicelib.infrastructure.dynamodb.model.task_model import TaskDynamoModel
from chalicelib.infrastructure.dynamodb.model.user_model import UserModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import DynamoIO


class TaskUserDynamoRepository(TaskUserRepository):
    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def register_task_user(self, task_user: TaskUser):
        user_model = UserModel.from_user(task_user._user)
        task_model_list = [
            TaskDynamoModel.from_task(task=task) for task in task_user._task_list
        ]
        self._dynamo_io.put_item(user_model)
        for task in task_model_list:
            self._dynamo_io.put_item(task)
