import json
import asyncio
import aiohttp
from lxml import etree


async def login(usn, dob):
    baseurl = "https://parents.msrit.edu/"

    dummy_response = {
        "usn": usn,
        "dob": dob,
        "dummy_data": "This is a dummy response for testing purposes",
        "ver": "0.1"
    }

    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            async with session.get(baseurl, headers=headers) as resp:
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
