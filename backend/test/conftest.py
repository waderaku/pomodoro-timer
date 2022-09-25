import subprocess
from test.common import TEST_PATH

import inject
import pytest
from app import inject_config
from chalicelib.util import load_env


@pytest.fixture(scope="session", autouse=True)
def setup_container():
    # すでにtest-dynamodb Containerが立ち上がっていた場合に備えて削除コマンドを走らせておく
    subprocess.run(r"docker stop test-dynamodb", shell=True)
    # test-dynamodbを立ち上げる。失敗したらエラーを吐く。
    try:
        subprocess.run(
            r"docker run --rm -d --name test-dynamodb --net=pomodoro-timer amazon/dynamodb-local",
            shell=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        print("すでにコンテナが存在するのでコンテナ立ち上げをスキップ")
    path = TEST_PATH.joinpath(".env")
    load_env(path)
    inject.clear_and_configure(inject_config)
    yield
    subprocess.run(r"docker stop test-dynamodb", shell=True)
