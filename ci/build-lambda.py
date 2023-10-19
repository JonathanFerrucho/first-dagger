import os
import sys

import anyio

import dagger


async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

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
            .with_exec(["mkdir", "host"])
            .with_exec(["zip", "-r", "./host/function.zip", "."])
            .with_workdir("/lambda/host")
            # .with_exec(["zip", "function.zip", "handler.py"])
        )

        export = (
            build
            .directory(".")
            .export("./host")
        )

        await export



    print(f"Build lambda finished")


anyio.run(main)