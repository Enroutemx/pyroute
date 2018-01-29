import unittest
from selenium import webdriver as wd
from pyroute.modules.webdriver import WebDriverModule

class WDTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config =  {
            "host": "http://127.0.0.1:4444/wd/hub",
            "url": "http://www.enroute.xyz",
            "timeout": "50000",
            "window_size": "maximize",
            "otro_param": "here",
            "desired_capabilities": {
                "browserName":"firefox",
                "version":"58"
                }
            }
        cls.I = WebDriverModule(config)
        cls.I.driver = wd.Remote(command_executor=cls.I.host, desired_capabilities=cls.I.capabilities)
        cls.I.current_tab = 0
        cls.I.tabs = []
        cls.I.driver.get(cls.I.page)

    def test_call_get_cookie_check_if_is_empty(self):
        resp = self.I.get_cookie('_ga')
        print(resp)
        self.assertIsNotNone(resp)

    def test_call_get_cookie_compare_with_exact_cookie(self):
        resp = self.I.get_cookie('_gat')
        test = {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.enroute.xyz', 'expiry': '1516993366', 'secure': 'False', 'httpOnly': 'False'}
        print(resp, test)
        self.assertNotEqual(resp, test)

    def test_call_get_cookie_compare_with_different_cookie(self):
        resp = self.I.get_cookie('_ga')
        test = self.I.get_cookie('_ga')
        self.assertEqual(resp, test)

if __name__ == '__main__':
    unittest.main()
