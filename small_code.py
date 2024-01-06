import json
import time
import requests
from lxml import etree
from bs4 import BeautifulSoup


def login(usn, dob):
    baseurl = "https://parents.msrit.edu/"

    dummy_response = {
        "usn": usn,
        "dummy_data": "This is a dummy response for testing purposes",
        "ver": "0.1"
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            # Add more headers if needed to mimic a real user agent
        }

        with requests.Session() as session:
            # Make an initial request to establish a session
            resp = session.get(baseurl, headers=headers)

            if resp.status_code == 200:
                # Delay before making the next request
                time.sleep(2)
                # You might need to extract and use cookies from the response headers
                cookies = resp.cookies

                # Make another request with the established session and cookies
                resp2 = session.get(baseurl, headers=headers, cookies=cookies)

                if resp2.status_code == 200:
                    soup = BeautifulSoup(resp2.content, 'html.parser')
                    title = soup.title.string
                    dummy_response['website_title'] = title if title else 'Title not found'
                else:
                    dummy_response['error'] = f"Received status code {resp2.status_code}"
            else:
                dummy_response['error'] = f"Received status code {resp.status_code}"

    except Exception as e:
        dummy_response['error'] = f"Error during scraping: {str(e)}"

    return dummy_response


def main(usn, dob):
    return login(usn, dob)

# def lambda_handler(event, context):
#     dob = event['queryStringParameters']['dob']
#     usn = event['queryStringParameters']['usn']
#     result = login(usn, dob)
#
#     return {
#         "statusCode": 200,
#         "body": json.dumps(result)
#     }
