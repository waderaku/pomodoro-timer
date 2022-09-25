from abc import ABC
from dataclasses import asdict, dataclass

from dacite import from_dict
from typing_extensions import Self


@dataclass
class DynamoModel(ABC):
    def as_dynamo_item(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dynamo_item(cls, item: dict) -> Self:
        return from_dict(cls, item)
