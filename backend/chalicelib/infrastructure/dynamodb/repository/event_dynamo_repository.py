from chalicelib.domain.model.entity.event import Event
from chalicelib.domain.repository.event_repository import EventRepository
from chalicelib.infrastructure.dynamodb.model.event_model import EventDynamoModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_repository import (
    DynamoRepository,
)


class EventDynamoRepository(EventRepository, DynamoRepository):
    def register_event(self, event: Event):
        dynamo_input = EventDynamoModel.from_event(event).to_dynamo_input()
        self._table.put_item(dynamo_input)
