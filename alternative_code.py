import asyncio
import json

import aiohttp
from lxml import etree

baseurl = "https://parents.msrit.edu"


async def scrape_login_dashboard(respobj):
    body = await respobj.content.read()
    dom = etree.HTML(body)
    firstScreenData = {'dom': dom.xpath('//title/text()')[0],
                       'status': f"Status: {respobj.status} | Reason: {respobj.reason}",
                       'url': f"URL: {respobj.url}",
                       'headers': f"Headers: {respobj.headers}"
                       }
    studdetailshead = dom.xpath(
        '//*[@class="cn-basic-details"]/table/tbody/tr/td/span/text()')
    studdetailstable = dom.xpath(
        '//*[@class="cn-basic-details"]/table/tbody/tr/td/text()')

    studimage_elements = dom.xpath(
        '//img[@class="uk-preserve-width uk-border"]/@src')
    if studimage_elements:
        studimage = studimage_elements[-1]
        firstScreenData['studentImage'] = baseurl + '/' + studimage
    else:
        firstScreenData['studentImage'] = 'default-image-url'

    for x, y in zip(studdetailshead, studdetailstable):
        firstScreenData[x.strip()] = y.strip()

    return firstScreenData


async def login(usn, dob):
    yy = dob[0:4]
    mm = dob[5:7]
    dd = dob[8:10]

    dummy_response = {
        "usn": usn,
    }

    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(baseurl) as resp:
                print(resp.url)
                body = await resp.content.read()
                dom = etree.HTML(body)
                try:
                    token = dom.xpath('//input[@value="1"]/@name')[0]
                except IndexError:
                    token = None
                print(f"token: {token}")
                data = {
                    'username': usn,
                    'dd': dd,
                    'mm': mm,
                    'yyyy': yy,
                    'passwd': dob,
                    'remember': 'No',
                    'option': 'com_user',
                    'task': 'login',
                    'return': '�w^Ƙi',
                    'return': '',
                    'ea07d18ec2752bcca07e20a852d96337': '1'
                }
                headers = {
                    'Referer': baseurl,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                cookies = session.cookie_jar.filter_cookies(resp.url)
                print(f"Cookie: {cookies}")
                dummy_response['cookies'] = cookies
                dummy_response['token'] = token
                async with session.post(resp.url, data=data, headers=headers) as resp2:
                    print(resp2)
                    x1 = await scrape_login_dashboard(resp2)
                    dummy_response.update(x1)
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


def sasa(usn, dob):
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(main(usn, dob))
    return {
        "statusCode": 200,
        "body": json.dumps(x)
    }
