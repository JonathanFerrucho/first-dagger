import json
import os
import sys

import anyio

import dagger

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)

async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # set AWS credentials as client secrets
        # aws_access_key_id = client.set_secret(
        #     "aws_access_key_id",
        #     os.environ["AWS_ACCESS_KEY_ID"],
        # )
        # aws_secret_access_key = client.set_secret(
        #     "aws_secret_access_key",
        #     os.environ["AWS_SECRET_ACCESS_KEY"],
        # )

        # aws_session_token = client.set_secret(
        #     "aws_session_token",
        #     os.environ["AWS_SESSION_TOKEN"],
        # )

        # aws_region = os.environ["AWS_DEFAULT_REGION"]


        # lambda_dir = client.host().directory(".", include=["host"]).directory("host")

        # build = (
        #     client.container()
        #     .from_("python:3.10-alpine")
        #     .with_directory("/host", lambda_dir)
        # )

        response = await (
            _lambda.Function(
                self, 'create-jira-issue',
                runtime=_lambda.Runtime.PYTHON_3_10,
                code=_lambda.Code.from_asset('/lambda'),
                handler='lambda.handler',
            )
        )
        data = json.loads(response)

    print(f"Function updated at: {data}")


anyio.run(main)