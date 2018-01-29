import unittest
from selenium import webdriver as wd
from pyroute.modules.webdriver import WebDriverModule

class WDTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config =  {
            "host": "http://127.0.0.1:4444/wd/hub",
            "url": "http://www.enroute.xyz/home/",
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

    def test_call_get_cookies_compare_with_exact_cookies(self):
         resp = self.I.get_cookies()
         test = self.I.get_cookies()
         print(resp, test)
         self.assertEqual(resp, test)

    def test_call_get_cookies_check_if_is_empty(self):
        resp = self.I.get_cookies()
        self.assertIsNotNone(resp)

    def test_call_get_cookie_verified_if_is_in_cookies(self):
        test = self.I.get_cookie('_session_id')
        resp = self.I.get_cookies()
        self.assertIn(test, resp)

if __name__ == '__main__':
    unittest.main()
