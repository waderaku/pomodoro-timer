#!/usr/bin/env python3
try:
    from aws_cdk import core as cdk
except ImportError:
    import aws_cdk as cdk

from stacks.chaliceapp import ChaliceApp
from stacks.s3_bucket import S3Bucket

app = cdk.App()
ChaliceApp(app, "backend")
S3Bucket(app, "frontend")

app.synth()
