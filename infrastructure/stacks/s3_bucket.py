from aws_cdk import RemovalPolicy, Stack
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import BucketDeployment, Source
from constant import PROJECT_ROOT

FRONTEND_SOURCE_DIR = PROJECT_ROOT.joinpath("frontend", "build")


class S3Bucket(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.bucket = Bucket(
            self,
            id="PomodoroTimerFrontendBucket",
            bucket_name="pomodoro-front-bucket-test",
            website_index_document="index.html",
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
        )
        self.deploy = BucketDeployment(
            self,
            "DeployPomodoro-frontend",
            sources=[Source.asset(str(FRONTEND_SOURCE_DIR))],
            destination_bucket=self.bucket,
        )
