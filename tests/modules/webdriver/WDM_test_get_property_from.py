import unittest
from selenium import webdriver as wd
from pyroute.modules.webdriver import WebDriverModule

class WDTest(unittest.TestCase):

"""
Not yet functional.
"""
		
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

    def test_call_get_property_compare_with_expected_value(self):
        resp = self.I.get_property_from({'xpath':'/html/body/div[1]'}, 'line-height')
        self.assertEqual(resp, 'visible')


if __name__ == '__main__':
    unittest.main()