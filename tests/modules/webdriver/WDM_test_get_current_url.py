import unittest
from selenium import webdriver as wd
from pyroute.modules.webdriver import WebDriverModule

class WDTest(unittest.TestCase):
		
    @classmethod
    def setUpClass(cls):
        config =  {
            "host": "http://127.0.0.1:4444/wd/hub",
            "url": "http://enroute.xyz/home/",
            "timeout": "50000",
            "window_size": "maximize",
            "otro_param": "here",
            "desired_capabilities": {
                "browserName":"firefox", 
                "version":"57"
                }	
            }
        cls.I = WebDriverModule(config)   
        cls.I.driver = wd.Remote(command_executor=cls.I.host, desired_capabilities=cls.I.capabilities)
        cls.I.current_tab = 0
        cls.I.tabs = []
        cls.I.driver.get(cls.I.page)

    @classmethod
    def tearDownClass(cls):
        cls.I.current_tab = {}
        cls.I.tabs = []
        cls.I.driver.quit()

    def test_call_get_current_url_validate_not_None(self):
        resp = self.I.get_current_url()
        self.assertIsNotNone(resp)

    def test_call_get_current_url_compare_with_expected_value(self):
        resp = self.I.get_current_url()
        url = 'http://enroute.xyz/home/'
        self.assertEqual(resp, url)

    def test_call_get_current_url_compare_with_empty_string(self):
        resp = self.I.get_current_url()
        url = ''
        self.assertNotEqual(resp, url)


if __name__ == '__main__':
    unittest.main()