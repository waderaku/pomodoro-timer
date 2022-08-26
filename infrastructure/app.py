#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.chaliceapp import ChaliceApp

app = cdk.App()
ChaliceApp(app, "backend")

app.synth()
