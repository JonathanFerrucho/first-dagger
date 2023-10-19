import os


def handler(event, context):
    print("entre al handler")
    print(f"{event}")
    print(f"{context}")
    return "entre al handler"