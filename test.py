import unittest
from app import app


class Test(unittest.TestCase):
    def test_getdata(self):
        tester = app.test_client()
        response = tester.get('/getdata?usn=1ms21is017&dob=2003-06-07')
        print(response.data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
