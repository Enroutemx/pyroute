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

    def test_call_get_element_size_compare_with_different_size(self):
        test = {'height': 808.0, 'width': 1270.0}
        resp = self.I.get_element_size({"xpath" : '/html/body/div[1]'})
        self.assertNotEqual(test, resp)

    def test_call_get_element_size_check_if_is_empty(self):
        resp = self.I.get_element_size({"xpath" : '/html/body/div[1]'})
        self.assertIsNotNone(resp)

    def test_call_get_element_size_compare_with_exact_size(self):
        test = {'height': 702.0, 'width': 1280.0}
        resp = self.I.get_element_size({"xpath" : '//*[@id="wrapper"]/div[5]'})
        self.assertEqual(test, resp)

if __name__ == '__main__':
    unittest.main()
