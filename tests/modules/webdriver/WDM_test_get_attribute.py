import unittest
from selenium import webdriver as wd
from pyroute.modules.webdriver import WebDriverModule


class WDTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = {
            "host": "http://127.0.0.1:4444/wd/hub",
            "url": "http://www.google.com.mx/",
            "timeout": "50000",
            "window_size": "maximize",
            "otro_param": "here",
            "desired_capabilities": {
                "browserName": "firefox",
                "version": "57"
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

    def test_call_get_attribute_button_invalid_attribute_name_yield_none(self):
        resp = self.I.get_attribute_from({'xpath': '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'}, 'color')
        self.assertIsNone(resp)

    def test_call_get_attribute_button_valid_attribute_name_yield_not_none(self):
        resp = self.I.get_attribute_from({'xpath': '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'}, 'jsaction')
        self.assertIsNotNone(resp)

    def test_call_get_attribute_button_name(self):
        resp = self.I.get_attribute_from({'xpath': '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'}, 'name')
        self.assertEqual(resp, "btnK")

    def test_call_get_attribute_button_value(self):
        resp = self.I.get_attribute_from({'xpath': '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'}, 'value')
        self.assertEqual(resp, "Buscar con Google")

    def test_call_get_attribute_button_type(self):
        resp = self.I.get_attribute_from({'xpath': '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'}, 'type')
        self.assertEqual(resp, "submit")


if __name__ == '__main__':
    unittest.main()
