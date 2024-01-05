import json
import asyncio
import aiohttp
from lxml import etree


async def login(usn, dob):
    baseurl = "https://parents.msrit.edu/"

    # Dummy response for testing
    dummy_response = {
        "usn": usn,
        "dummy_data": "This is a dummy response for testing purposes",
        "ver": "0.1"  # Update with the desired version
    }

    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(baseurl) as resp:
                body = await resp.content.read()
                dom = etree.HTML(body)
                title = dom.xpath('//title/text()')
                dummy_response['website_title'] = title[0] if title else 'Title not found'
    except Exception as e:
        dummy_response['error'] = f"Error during scraping: {str(e)}"

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
