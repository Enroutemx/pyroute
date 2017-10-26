from pyroute.module import Module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert


class Webdriver(Module):
    def __init__(self, config, **kwargs):

        # Default values
        self.defaults = {
            "window_size": "maximize"
        }

        # Load configuration parameters from config.json
        self.config_data = super().\
            __init__(config=config, defaults=self.defaults)
        self.module_config = self.config_data['defaults']

        # Check that the required fields are present 
        self.__check_required_fields()

        # Parameters to set browser configurations
        self.host = self.module_config['host']
        self.page = self.module_config['url']
        self.window_size = self.module_config['window_size']
        self.capabilities = self.module_config['desired_capabilities']

        # Set driver to start an instance
        self.driver = webdriver.Remote(command_executor = self.host,
                            desired_capabilities = self.capabilities)

        # Run private methods to set the browser configurations
        self.__window_size()

    def __check_required_fields(self):
        try:
            assert 'host' in self.module_config.keys() and \
                                'url' in self.module_config.keys()
        except KeyError as ke:
            ke.args('Required keys are not stored at config.json')

    def __window_size(self):
        if self.window_size == 'maximize':
            self.driver.maximize_window()
        else:
            x = self.window_size.index('x')
            window_width = self.window_size[:x]
            window_height = self.window_size[x+1:]
            self.driver.set_window_size(window_width,window_height)

    def accept_alert(self):
        WebDriverWait(self.driver ,3).until(ec.alert_is_present(),'')
        self.driver.switch_to.alert.accept()

    def append_text(self, selector, text):
        append_text = self.get_text_from(selector) + text
        self.fill_field(selector, append_text)

    # moves the browser to the especified page
    def am_on_page(self, path):
        if path == '/':
            self.driver.get(self.page)
        else:
            self.driver.get(self.page+path)

    def cancel_popup(self):
         Alert(self.driver).dismiss()
    
    def check_option(self, selector):
        self._search_element(selector).click

    def clear_fill(self, selector):
        self._search_element(selector).clear()

    # click on the selected element
    def click(self, selector):
        self._search_element(selector).click()

    # close the current window
    def close(self):
        self.driver.close()

    def add_cookie(self, name, value):
        self.driver.add_cookie({'name': name, 'value': value})

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def delete_cookie(self, name):
        self.driver.delete_cookie(name)

    def double_click(self, selector):
        element = self._search_element(selector)
        ActionChains.double_click(element)

    def execute_script(self, script, *args):
        self.driver.execute_script(script, *args)

    def execute_async_script(self, script, *args):
        self.driver.execute_async_script(script, *args)

    # Type 'string' in the element 'x'
    def fill_field(self, selector, text):
        self._search_element(selector).send_keys(text)

    def get_browser_logs(self):
        self.driver.get_log('browser')

    def get_cookie(self, name):
        return self.driver.get_cookie(name)

    def get_cookies(self):
        return self.driver.get_cookies()

    def get_source(self, selector):
        return self._search_element(selector).get_attribute('innerHTML')

    def get_attribute_from(self, selector, name):
        element = self._search_element(selector)
        return element.get_attribute(name)

    def get_current_url(self):
        return self.driver.current_url

    def get_property_from(self, selector, name):
        element = self._search_element(selector)
        return element.get_property(name)

    # Is needed a dict to return the text of the given element
    # {'type of selector':'selector'}
    def get_text_from(self, selector):
        return self._search_element(selector).text

    def get_element_size(self, selector):
        return self._search_element(selector).size

    def get_title(self):
        return self.driver.title

    def go_back(self):
        self.driver.back()

    def go_foward(self):
        self.driver.forward()

    def maximize_window(self):
        self.driver.maximize_window()

    def open_a_webpage(self, source):
        self.driver.get(source)

    def scroll_to(self, selector):
        element_position = self._search_element(selector).location
        self.driver.execute_script("window.scrollTo(0,"+str(element_position['y'])+");")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollTop);")

    # returns True if element is displayed and False if not
    def see_element(self, selector):
        try:
            assert self._search_element(selector).is_displayed()
        except NoSuchElementException:
            assert False

    # returns True if element is clickable and False if not
    def see_element_clickable(self, selector):
        try:
            assert self._search_element(selector).is_enabled()
        except NoSuchElementException:
            assert False

    # Can be used to check if a checkbox or radio button is selected.
    def see_selected_element(self, selector):
        try:
            assert self._search_element(selector).is_selected()
        except NoSuchElementException:
            assert False

    # timeouts should receive a dictionary
    # example: {'page_load':x,'script':y}
    def set_timeout(self, timeouts):
        if timeouts['page_load'] is not None:
            self.driver.set_page_load_timeout(timeouts['page_load'])
        if timeouts['script'] is not None:
            self.driver.set_script_timeout(timeouts['script'])

    def set_window_position(self, x, y):
        self.driver.set_window_position(x, y)

    def submit_a_form(self, selector):
        self._search_element(selector).submit()

    def refresh_page(self):
        self.driver.refresh()

    def resize_window(self, window_size):
        x = window_size.index('x')
        window_width = window_size[:x]
        window_height = window_size[x+1:]
        self.driver.set_window_size(window_width,window_height)

    # takes a screenshot of the current page, and it will be a PNG
    # You can add a the path to where wou want to save the screen shot
    # example: I.take_a_screenshot('screenshots/test.png')
    def take_a_screenshot(self, path):
        self.driver.save_screenshot(path)

    # example I.take_a_screen_shot_element('/Screenshots/foo.png')
    def take_a_screenshot_element(self, selector, path):
        element = self._search_element(selector)
        element.screenshot(path)

    def wait(self, time):
        self.driver.implicitly_wait(time)

    def wait_for_element(self, selector, time):
        if self.see_element(selector) is not True:
            self.wait(time)

    def wait_for_enable(self, selector, time):
        if self.see_element_clickable(selector) is not True:
            self.wait(time)

    def wait_for_text(self, text, selector, time):
        if self.get_text_from(selector) is not text:
            self.wait(time)

    def wait_url_equals(self, url, time):
        current_url = self.driver.current_url
        if current_url != url:
            self.wait(time)
            self.wait_url_equals(url, time)

    def _search_element(self, full_selector):
        if 'css' in full_selector.keys():
            element = self.driver.find_element_by_css_selector(
                full_selector['css'])
        elif 'xpath' in full_selector.keys():
            element = self.driver.find_element_by_xpath(full_selector['xpath'])
        elif'id' in full_selector.keys():
            element = self.driver.find_element_by_id(full_selector['id'])
        elif 'name' in full_selector.keys():
            element = self.driver.find_element_by_name(full_selector['name'])
        else:
            print('Incorrect Selector type')
        return (element)
