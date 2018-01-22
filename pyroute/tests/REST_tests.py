import unittest

from pyroute.modules.REST import RestModule


class RESTTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = {
            "timeout": "50000",
            "endpoint": "http://google.com",
            "reset_headers": "True",
            "otro_param": "here"
            }

        cls.rest = RestModule(config)

    def test_send_get_request_with_valid_url(self):
        resp = self.rest.send_get_request('/')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
