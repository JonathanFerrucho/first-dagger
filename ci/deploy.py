import os
import sys

import anyio

import dagger


async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        out = await (
            client.container()
            .from_("alpine:latest")
            .with_directory("/", client.host().directory("/home/circleci/project"))
            .with_exec(["ls", "."])
            .stdout()
        )

    print(out)


anyio.run(main)