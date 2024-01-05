import json
import asyncio


async def login(usn, dob):
    dummy_response = {
        "usn": usn,
        "dob": dob,
        "dummy_data": "This is a dummy response for testing purposes",
        "ver": "0.1"
    }
    return dummy_response


async def main(usn, dob):
    x = await login(usn, dob)
    return x


def lambda_handler(event, context):
    dob = event['queryStringParameters']['dob']
    usn = event['queryStringParameters']['usn']
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(usn, dob))

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
