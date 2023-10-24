import json
import os
import sys

import anyio

import dagger
import boto3


async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        # get reference to function directory
        lambda_dir = client.host().directory(".", include=["host"]).directory("host")

        # use a node:18-alpine container
        # mount the function directory
        # at /src in the container
        # install application dependencies
        # create zip archive
        build = (
            client.container()
            .from_("python:3.10-alpine")
            .with_directory("/host", lambda_dir)
        )

        lambda_client = boto3.client('lambda')

        # add zip archive to AWS CLI container
        # use CLI commands to deploy new zip archive
        # and get function URL
        # parse response and print URL
        response = await (
            lambda_client.update_function_code(
                FunctionName="create-jira-issue",
                ZipFile= build.file("/host/function.zip")
            )
        )
        data = json.loads(response)

    print(f"Function updated at: {data}")


anyio.run(main)