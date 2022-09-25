from dataclasses import asdict, dataclass


@dataclass
class DynamoKey:
    """PomodoroTimerテーブル専用のキーオブジェクト"""

    ID: str
    DataType: str

    def as_dynamo_key(self) -> dict:
        return asdict(self)
