from aws_cdk import aws_dynamodb as dynamodb

try:
    from aws_cdk import core as cdk
except ImportError:
    import aws_cdk as cdk

from chalice.cdk import Chalice
from constant import PROJECT_ROOT

CHALICELIB_SOURCE_DIR = PROJECT_ROOT.joinpath("backend")
assert CHALICELIB_SOURCE_DIR.exists()


class ChaliceApp(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.dynamodb_table = self._create_ddb_table()
        self.chalice = Chalice(
            self,
            "ChaliceApp",
            source_dir=str(CHALICELIB_SOURCE_DIR),
            stage_config={
                "environment_variables": {
                    # 'APP_TABLE_NAME': self.dynamodb_table.table_name,
                    "ENV": "prod"
                }
            },
        )
        self.dynamodb_table.grant_read_write_data(self.chalice.get_role("DefaultRole"))

    def _create_ddb_table(self):
        dynamodb_table = dynamodb.Table(
            self,
            "pomodoro_info",
            table_name="pomodoro_info",
            partition_key=dynamodb.Attribute(
                name="ID", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="DataType", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            # 一旦読み書きのキャパシティを5ユニットに設定。随時調整
            read_capacity=5,
            write_capacity=5,
        )
        dynamodb_table.add_local_secondary_index(
            sort_key=dynamodb.Attribute(
                name="DataValue", type=dynamodb.AttributeType.STRING
            ),
            index_name="dataValueLSIndex",
            projection_type=dynamodb.ProjectionType.ALL,
        )
        cdk.CfnOutput(self, "AppTableName", value=dynamodb_table.table_name)
        return dynamodb_table
