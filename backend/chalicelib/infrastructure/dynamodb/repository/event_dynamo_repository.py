from boto3.dynamodb.conditions import Key
from chalicelib.domain.model.entity.event import Event
from chalicelib.domain.repository.event_repository import EventRepository
from chalicelib.infrastructure.dynamodb.model.event_model import EventDynamoModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import DynamoIO


class EventDynamoRepository(EventRepository):
    def __init__(self, dynamo_io: DynamoIO):
        self._dynamo_io = dynamo_io

    def register_event(self, event: Event):
        self._upsert_event(event)

    def fetch_by_user_id(self, user_id: str) -> list[Event]:
        condition = Key("ID").eq(f"{user_id}_event")
        event_dynamo_list = self._dynamo_io.query(condition, EventDynamoModel)
        return [dynamo_model.to_event() for dynamo_model in event_dynamo_list]

    def update_event(self, event: Event):
        self._upsert_event(event)

    def _upsert_event(self, event: Event):
        dynamo_model = EventDynamoModel.from_event(event)
        self._dynamo_io.put_item(dynamo_model)
