import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from pyroute.module import Module
# This will be used later
# from selenium.common.exceptions import HCExceptions


class Headlesschrome(Module):

    def __init__(self, config, **kwargs):

        # Default values
        self.defaults = {
            "chromedriver_path": "/usr/lib/chromium-browser/chromedriver",
            "chrome_path": "/usr/bin/chromium-browser",
            "url": "https://enroute.xyz"
        }
        self.config_data = super().\
            __init__(config=config, defaults=self.defaults)

        self.module_config = self.config_data['defaults']
        url = self.module_config["url"]
        path = self.module_config["chromedriver_path"]
        self._element_queue = []

        # Set all options
        self._c_options = Options()
        self._c_options.add_argument("--headless")
        self._c_options.binary_location = self.module_config["chrome_path"]

        # The service is needed to actually start the browser
        self._service = webdriver.chrome.service.Service(path)
        self._service.start()
        self._start_browser(url, path, self._c_options)

    def _init(self):
        pass

    def _before_init(self):
        pass

    def _after_init(self):
        pass

    def _check_requirements(self):
        """Implementation pending"""
        pass

    # Browser Methods
    def _start_browser(self, url, driver_path, options):
        self._driver = webdriver.Chrome(executable_path=driver_path,
                                        chrome_options=options)
        self._driver.get(url)

    def go_forward(self):
        self._driver.forward()

    def go_back(self):
        self._driver.back()

    def set_cookies(self, **cookies):
        for cookie_key, cookie_val in cookies.items():
            cookie = dict(name=cookie_key, value=cookie_val)
            self._driver.add_cookie(cookie)

    def get_cookies(self):
        self._driver.get_cookies()

    def end(self):
        """
        This method closes the current page and terminates
        the driver, used at the end of a test
        """
        self._driver.close()
        self._driver.quit()

    @property
    def am_on(self):
        """
        This method returns the current page
        """
        return self._driver.current_url

    def go_to(self, url):
        """
        This method changes the current page to a new url
        param: url - The URL to access
        """
        self._driver.get(url)
    # Assertions
    def confirm_title_includes(self, string):
        return string in self._driver.title 

    def page_title(self):
        return self._driver.title

    # Search and Selectors
    def select_by_class(self, class_attr):
        self._element_queue.append(self._driver.find_element_by_css_selector(class_attr))
    
    def select_by_xpath(self, xpath):
        self._element_queue.append(self._driver.find_element_by_xpath(xpath))

    def press(self, text):
        element = self._element_queue.pop()
        element.send_keys(text)

    def fill_in(self, text):
        element = self._element_queue.pop()
        element.send_keys(text)
        element.send_keys(Keys.RETURN)
    
    def click_button(self):
        element = self._element_queue.pop()
        element.click()

    # Interactions
    # Interactions are begun when a test starts,
    # these methods will be used then
    def _start_interactions(self, driver):
        self._interaction_queue = ActionChains(driver)

    def _execute_interactions(self):
        self._interaction_queue.perform()

    def click(self, target):
        self._interaction_queue.click(target)

    def right_click(self, target):
        self._interaction_queue.context_click(target)

    def double_click(self, target):
        self._interaction_queue.double_click(target)

    def click_and_keep_pressed(self, target):
        self._interaction_queue.click_and_hold(target)

    def move_cursor_to(self, target):
        self._interaction_queue.move_to_element(target)

    def move_cursor_to_position(self, x_offset, y_offset):
        self._interaction_queue.move_to_offset(x_offset, y_offset)

    # This will be used by and for the DOM search engine,
    # to find elements easily
    def _dump_DOM(self):
        pass
