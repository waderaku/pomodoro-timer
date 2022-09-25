from __future__ import annotations

from typing import Optional, Protocol, TypeVar

from boto3.dynamodb.conditions import ConditionBase
from chalicelib.domain.repository.repository import BatchWriter
from chalicelib.infrastructure.dynamodb.model.dynamo_model import DynamoModel
from chalicelib.infrastructure.dynamodb.repository.dynamo_key import DynamoKey


class DynamoTableProtocol(Protocol):
    def put_item(self, Item):
        raise NotImplementedError

    def delete_item(self, Key):
        raise NotImplementedError


T = TypeVar("T", bound=DynamoModel)


class DynamoIO(BatchWriter):
    def __init__(self, table):
        self._table = table
        self._batch = None

    def put_item(self, item: DynamoModel):
        table = self._batch_or_table()
        table.put_item(item.as_dynamo_item())

    def delete_item(self, key: DynamoKey):
        table = self._batch_or_table()
        table.delete_item(key.as_dynamo_key())

    def get_item(self, key: DynamoKey, Model: type[T]) -> T:
        return Model(**self._table.get_item(key.as_dynamo_key())["Item"])

    def query(self, condition: ConditionBase, Model: type[T]) -> list[T]:
        item_list = self._table.query(KeyConditionExpression=condition)["Items"]
        return [Model.from_dynamo_item(item) for item in item_list]

    def __enter__(self):
        self._batch = self._table.batch_writer().__enter__()

    def __exit__(self):
        self._batch = None
        self._table.batch_writer().__exit__()

    def _batch_or_table(self) -> DynamoTableProtocol:
        if self._batch_writer.batch:
            return self._batch_writer.batch
        else:
            return self._table

    @property
    def batch(self) -> Optional[DynamoTableProtocol]:
        return self._batch
