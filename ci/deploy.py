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
            .with_directory("/host", client.host().directory("app"))
            .with_exec(["ls", "-la", "host"])
            .stdout()
        )

    print("out")
    print(out)


anyio.run(main)