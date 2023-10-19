import json
import os
import sys

import anyio

import dagger


async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # set AWS credentials as client secrets
        aws_access_key_id = client.set_secret(
            "aws_access_key_id",
            os.environ["AWS_ACCESS_KEY_ID"],
        )
        aws_secret_access_key = client.set_secret(
            "aws_secret_access_key",
            os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        aws_secret_access_key = client.set_secret(
            "aws_session_token",
            os.environ["AWS_SESSION_TOKEN"],
        )

        aws_region = os.environ["AWS_DEFAULT_REGION"]

        # get reference to function directory
        lambda_dir = client.host().directory(".", include=["lambda"]).directory("lambda")

        # use a node:18-alpine container
        # mount the function directory
        # at /src in the container
        # install application dependencies
        # create zip archive
        build = (
            client.container()
            .from_("python:3.10-alpine")
            .with_exec(["apk", "add", "zip"])
            .with_directory("/lambda", lambda_dir)
            .with_workdir("/lambda")
            # .with_exec(
            #     ["pip", "install", "--target", "./packages", "-r", "requirements-dod.txt"]
            # )
            .with_workdir("/lambda/packages")
            .with_exec(["zip", "-r", "../function.zip", "."])
            .with_workdir("/lambda")
            .with_exec(["zip", "function.zip", "handler.py"])
        )

        # use an AWS CLI container
        # set AWS credentials and configuration
        # as container environment variables
        aws = (
            client.container()
            .from_("amazon/aws-cli:2.11.22")
            .with_secret_variable("AWS_ACCESS_KEY_ID", aws_access_key_id)
            .with_secret_variable("AWS_SECRET_ACCESS_KEY", aws_secret_access_key)
            .with_env_variable("AWS_DEFAULT_REGION", aws_region)
        )

        # add zip archive to AWS CLI container
        # use CLI commands to deploy new zip archive
        # and get function URL
        # parse response and print URL
        response = await (
            aws.with_file("/tmp/function.zip", build.file("/lambda/function.zip"))
            .with_exec(
                [
                    "lambda",
                    "update-function-code",
                    "--function-name",
                    "create-jira-issue",
                    "--zip-file",
                    "fileb:///tmp/function.zip",
                ]
            )
            .with_exec(
                ["lambda", "get-function-url-config", "--function-name", "create-jira-issue"]
            )
            .stdout()
        )
        data = json.loads(response)

    print(f"Function updated at: {data['FunctionUrl']}")


anyio.run(main)