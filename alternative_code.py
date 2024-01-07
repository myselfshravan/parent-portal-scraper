import asyncio
import json

import aiohttp
from lxml import etree

baseurl = "https://parents.msrit.edu/"


async def scrape_login_dashboard(respobj):
    body = await respobj.content.read()
    dom = etree.HTML(body)
    firstScreenData = {}
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
    tables = dom.xpath(
        '//*[@class="uk-table uk-table-striped uk-table-hover cn-pay-table uk-table-middle"]')
    refunds = []
    fees = []

    for table in tables:
        capt = table.xpath('./caption/text()')[0]
        if capt == "Payment Updated":
            head = [i.strip() for i in table.xpath('.//thead/tr/th//text()')]
            for row in table.xpath('./tbody/tr'):
                d = {}
                for h, data in zip(head, row.xpath('./td//text()')):
                    d[h] = data.strip()
                fees.append(d)

        elif capt == "Refund Details":
            head = [i.strip() for i in table.xpath('.//thead/tr/td//text()')]
            for row in table.xpath('./tbody/tr'):
                d = {}
                for h, data in zip(head, row.xpath('./td//text()')):
                    d[h] = data.strip()
                refunds.append(d)

    firstScreenData['refunds'] = refunds
    firstScreenData['fees'] = fees
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
                # token = dom.xpath('//input[@value="1"]/@name')[0]
                # print(f"token: {token}")
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
                async with session.post(resp.url, data=data) as resp2:
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

