from pyroute.module import Module
from selenium.webdriver import remote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class Webdriver(Module):
    def __init__(self):
        capabilities = Module.super()
        self.host = capabilities['host']
        self.page = capabilities['page']
        self.driver = remote.webdriver.WebDriver(
            self.host, capabilities)

    def append_text(self, selector, text):
        append_text = self.get_text_from(selector) + text
        self.fill_field(selector, append_text)

    # moves the browser to the especified page
    def am_on_page(self, path):
        if path == '/':
            self.driver.get(self.page)
        else:
            self.driver.get(self.page+path)

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
        self.driver.execute_script(script,*args)

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
        return self._search_element(selector).is_displayed()

    # returns True if element is clickable and False if not
    def see_element_clickable(self, selector):
        return self._search_element(selector).is_enabled()

    # Can be used to check if a checkbox or radio button is selected.
    def see_selected_element(self, selector):
        return self._search_element(selector).is_selected()

    # timeouts should receive a dictionary
    # example: {'page_load':x,'script':y}
    def set_timeout(self, timeouts):
        if timeouts['page_load'] is not None:
            self.driver.set_page_load_timeout(timeouts['page_load'])
        if timeouts['script'] is not None:
            self.driver.set_script_timeout(timeouts['script'])

    def set_window_position(self, x, y):
        self.driver.set_window_position(x, y)

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    def submit_a_form(self, selector):
        self._search_element(selector).submit()

    def refresh_page(self):
        self.driver.refresh()

    def resize_window(self, width, height):
        self.driver.set_window_size(width, height)

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
