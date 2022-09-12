from pathlib import Path
from typing import Union
from dotenv import load_dotenv
import os


NECESSARY_ENVS = [
    "DYNAMODB_ENDPOINT",
    "AWS_DEFAULT_REGION",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
]


def load_env(path: Union[str, Path]):
    load_dotenv(path)
    assert all(val in os.environ for val in NECESSARY_ENVS)
