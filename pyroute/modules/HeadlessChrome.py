import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# This will be used later
# from selenium.common.exceptions import HCExceptions


class HeadlessChrome(object):

    def __init__(self):
        self._config = self._read_config('HC_config.json')
        self._check_requirements()
        self._before_init()
        self._init()
        self._after_init()
        url = self._config["url"]
        path = self._config["chromedriver_path"]
        self._start_browser(url, path, self._c_options)

    def _init(self):
        path = self._config["chromedriver_path"]
        self._service = webdriver.chrome.service.Service(path)
        self._service.start()

    def _before_init(self):
        pass

    def _after_init(self):
        self._c_options = Options()
        self._c_options.add_argument("--headless")
        self._c_options.binary_location = self._config["chrome_path"]

    def _check_requirements(self):
        """Implementation pending"""
        pass

    # A method to read a config file is common to all modules,
    # these should be defined in the Module Class
    def _read_config(self, config_file):
        def _is_valid_config():
            pass
        with open(config_file) as config_data:
            return json.load(config_data)

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
    def current_page(self):
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
