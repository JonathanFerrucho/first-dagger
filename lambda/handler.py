import os


def handler(event, context):
    print("entre al handler Test 2")
    print(f"{event}")
    print(f"{context}")
    return "entre al handler"