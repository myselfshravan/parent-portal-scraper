import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup

baseurl = "https://parents.msrit.edu/"


async def scrape_login_dashboard(respobj):
    body = await respobj.content.read()
    soup = BeautifulSoup(body.decode('latin1'))
    firstScreenData = {}

    return firstScreenData


async def login(usn, dob):
    dummy_response = {
        "usn": usn,
        "dob": dob,
        "dummy_data": "This is a dummy response for testing purposes",
        "ver": "0.1"
    }

    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(baseurl) as resp:
                body = await resp.content.read()
                soup = BeautifulSoup(body.decode('latin1'))
                title = soup.title.string if soup.title else 'Title not found'
                input_element = soup.find('input', {'value': '1'})
                token = input_element['name'] if input_element else 'Token not found'
                dummy_response['website_title'] = title
                dummy_response['token'] = token
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
