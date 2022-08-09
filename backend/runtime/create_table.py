import os
from pathlib import Path

import boto3

from chalicelib.util import load_env


def create_table():
    resource = boto3.resource(
        "dynamodb",
        endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", None),
    )
    table_name = "pomodoro_info"
    table = resource.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "ID", "AttributeType": "S"},
            {"AttributeName": "DataType", "AttributeType": "S"},
            {"AttributeName": "DataValue", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "ID", "KeyType": "HASH"},
            {"AttributeName": "DataType", "KeyType": "RANGE"},
        ],
        LocalSecondaryIndexes=[
            {
                "IndexName": "dataValueLSIndex",
                "KeySchema": [
                    {"AttributeName": "ID", "KeyType": "HASH"},
                    {"AttributeName": "DataValue", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    return table


if __name__ == "__main__":
    load_env(Path().joinpath("src", "app", ".env"))
    create_table()
