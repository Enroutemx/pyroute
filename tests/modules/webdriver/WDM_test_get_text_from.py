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

    def test_call_get_text_from_compare_with_exact_text(self):
        test = 'Home'
        resp = self.I.get_text_from({"xpath" : '//*[@id="wrapper"]/div[2]/div/div/div[2]/a[1]/p'})
        self.assertEqual(test, resp)

    def test_call_get_text_from_compare_with_different_text(self):
        test = 'Solution'
        resp = self.I.get_text_from({"xpath" : '//*[@id="wrapper"]/div[2]/div/div/div[2]/a[1]/p'})
        self.assertNotEqual(test, resp)

if __name__ == '__main__':
    unittest.main()
