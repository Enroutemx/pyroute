"""
The webdriver module wraps the selenium webdriver API and lets the user
conduct in-browser tests using the ITester's 'I' object.
"""
from pyroute.module import Module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
import time


class WebDriverModule(Module):
    def __init__(self, config, **kwargs):

        # Default values
        self.defaults = {
            "window_size": "maximize",
            "timeout": 10
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
        self.timeout = self.module_config['timeout']
        self.capabilities = self.module_config['desired_capabilities']

    def __setup_driver(self, source):
        self.driver = webdriver.Remote(command_executor=self.host,
                                       desired_capabilities=self.capabilities)
        if self.capabilities['browserName'] == 'chrome':
            self.current_tab = (0, source)
            self.tabs = [self.current_tab]
        elif self.capabilities['browserName'] == 'firefox':
            self.current_tab = 0
            self.tabs = [source]
        self.__window_size()

    def __check_required_fields(self):
        try:
            assert 'host' in self.module_config.keys() and\
                                'url' in self.module_config.keys()
        except KeyError as ke:
            ke.args('Required keys are not stored at config.json')

    def __window_size(self):
        if self.window_size == 'maximize' and not \
           self.capabilities['browserName'] == 'firefox':
            self.driver.maximize_window()

        elif not self.window_size == 'maximize':
            window_width, window_height = self.window_size.split('x')
            self.driver.set_window_size(window_width, window_height)

    def accept_alert(self):
        """
        This method searches for an Alert and accept it if found.
        """
        WebDriverWait(self.driver, self.timeout).\
            until(ec.alert_is_present(), '')
        self.driver.switch_to.alert.accept()

    def append_text(self, selector, text):
        """
        This method appends selected text with provided text.

        :param selector: Element selector.
        :type selector: str.
        :param text: Text to append to selected element.
        :type selector: str.
        """
        append_text = self.get_text_from(selector) + text
        self.fill_field(selector, append_text)

    # moves the browser to the especified page
    def am_on_page(self, path):
        """
        This method moves the browser to the specified page.

        :param path: Page path.
        :type path: str.
        """
        if path == '/':
            self.driver.get(self.page)
        else:
            self.driver.get(self.page+path)

    def attach_file(self, selector, path):
        """
        This method attaches a file.

        :param selector: Element selector.
        :type selector: str.
        :param path: File path.
        :type path: str.
        """
        self.driver._is_remote = False
        self._search_element(selector).clear()
        self._search_element(selector).send_keys(path)
        self.driver._is_remote = True

    def cancel_popup(self):
        """
        This method dissmisses an Alert.
        """
        Alert(self.driver).dismiss()

    def check_option(self, selector):
        """
        This method can check an input element by clicking it.

        :param selector: Element selector.
        :type selector: str.
        """
        self._search_element(selector).click()

    def clear_fill(self, selector):
        """
        This method can clear a selected input element.

        :param selector: Element selector.
        :type selector: str.
        """
        self._search_element(selector).clear()

    # click on the selected element
    def click(self, selector):
        """
        This method clicks the selected element.

        :param selector: Element selector.
        :type selector: str.
        """
        self._search_element(selector).click()

    # close the current tab
    def close_tab(self):
        """
        This method closes the current browser window.
        """
        self.driver.close()

    def copy_link(self, selector):
        """
        This method copies the selected href element.

        :param selector: Element selector.
        :type selector: str.
        :returns: The 'href' link.
        """
        element = self._search_element(selector)
        return element.get_attribute('href')

    def add_cookie(self, name, value):
        """
        This method adds a cookie using a name-value pair.

        :param name: Name value of the cookie.
        :param value: Value for the given cookie.
        :type name: str.
        :type value: str.
        """
        self.driver.add_cookie({'name': name, 'value': value})

    def delete_all_cookies(self):
        """
        This method deletes all browser cookies.
        """
        self.driver.delete_all_cookies()

    def delete_cookie(self, name):
        """
        This method deletes the specified cookie by name.

        :param name: Name of the cookie to delete.
        :type name: str.
        """
        self.driver.delete_cookie(name)

    def double_click(self, selector):
        """
        This method double clicks on the element using ActionChains.

        :param selector: Element selector.
        :type selector: str.
        """
        element = self._search_element(selector)
        ActionChains.double_click(element)

    def drag_and_drop(self, source, target):
        """
        This method enables drag and drop from a source to a target browser
        window.

        :param source: Element selector.
        :param target: Target X,Y coordinates.
        :type source: str.
        :type target: str.
        """
        s_element = self._search_element(source)
        if self.capabilities['browserName'] == 'chrome':
            if type(target) == str and 'x' in target and s_element:
                x, y = target.split('x')
                if x.isdigit() and y.isdigit():
                    ActionChains(self.driver).\
                     drag_and_drop_by_offset(s_element, int(x), int(y)).\
                     perform()
                    return

        elif self.capabilities['browserName'] == 'firefox':
            x, y = int(s_element.location['x']), int(s_element.location['y'])

            if type(target) == str and 'x' in target and s_element:
                x_t, y_t = target.split('x')
                if x_t.isdigit() and y_t.isdigit():
                    x = x + int(x_t)
                    y = y + int(y_t)
                    ActionChains(self.driver).\
                        drag_and_drop_by_offset(s_element, x, y).perform()
                    return

        t_element = self._search_element(target)
        ActionChains(self.driver).drag_and_drop(s_element,
                                                t_element).perform()

    def execute_script(self, script, *args):
        """
        This method executes a script using 'execute_script'.

        :param script: Script to execute.
        :param *args: Additional script arguments.
        :type script: str.
        """
        self.driver.execute_script(script, *args)

    def execute_async_script(self, script, *args):
        """
        This method executes a script asynchronously using
        'execute_async_script'.

        :param script: Script to execute.
        :param *args: Additional script arguments.
        :type script: str.
        """
        self.driver.execute_async_script(script, *args)

    # Type 'text' in the element 'selector'
    def fill_field(self, selector, text):
        """
        This method fills an input field with the provided text.

        :param selector: Input element selector to fill.
        :param text: Text to fill the element with.
        :type selector: str.
        :type text: str.
        """
        self._search_element(selector).send_keys(text)

    def get_browser_logs(self):
        """
        This method gets the browser logs.
        """
        self.driver.get_log('browser')

    def get_cookie(self, name):
        """
        This method fetches a specified cookie from the browser.

        :param name: Name of the Cookie.
        :type name: str.
        :returns: The specified Cookie.
        """
        return self.driver.get_cookie(name)

    def get_cookies(self):
        """
        This method gets all the browser cookies.

        :returns: All of the browser cookies.
        """
        return self.driver.get_cookies()

    def get_source(self, selector):
        """
        This method gets the source HTML of an element.

        :param selector: The element selector.
        :type selector: str.
        :returns: The specified element inner HTML.
        """
        return self._search_element(selector).get_attribute('innerHTML')

    def get_attribute_from(self, selector, name):
        """
        This method gets a specified browser cookie.

        :param name: The name of the cookie to get.
        :type name: str.
        :returns: Specified browser cookie.
        """
        element = self._search_element(selector)
        return element.get_attribute(name)

    def get_current_url(self):
        """
        This method gets the current browser URL.

        :returns: The current browser URL.
        """
        return self.driver.current_url

    def get_property_from(self, selector, name):
        """
        This method gets a property from a specified element.

        :param selector: The element selector.
        :type selector: str.
        :param name: The name of the element's property.
        :type name: str.
        :returns: The specified element's property.
        """
        element = self._search_element(selector)
        return element.get_property(name)

    def get_text_from(self, selector):
        """
        This method gets the text from an element.

        :param selector: The specified element selector.
        :type selector: str.
        :returns: Specified element's text.
        """
        return self._search_element(selector).text

    def get_element_size(self, selector):
        """
        This method gets the size from an element.

        :param selector: The specified element selector.
        :type selector: str.
        :returns: Specified element's size.
        """
        return self._search_element(selector).size

    def get_title(self):
        """
        This method gets the title from an element.

        :param selector: The specified element selector.
        :type selector: str.
        :returns: Specified element's title.
        """
        return self.driver.title

    def go_back(self):
        """
        This method goes one step backward in the browser history.
        """
        self.driver.back()

    def go_forward(self):
        """
        This method goes one step forward in the browser history.
        """
        self.driver.forward()

    def maximize_window(self):
        """
        This method maximize the browser window.
        """
        self.driver.maximize_window()

    def open_a_webpage(self, source):
        """
        This method can open a specific webpage in the current browser window.

        :param source: The specified webpage url.
        :type source: str.
        """
        self.__setup_driver(source)
        self.driver.get(source)

    def open_new_tab(self, source=''):
        """
        This method opens a new tab in the current browser window.

        :param source: The specified url for the new browser tab.
        :type source: str.
        """
        self.driver.execute_script("window.open('%s');" % source)

        if self.capabilities['browserName'] == 'chrome':

            new_win = self.driver.window_handles[-1]
            self.driver.switch_to_window(new_win)
            indx = self.tabs.index(self.current_tab)
            self.tabs.insert(indx+1, (len(self.tabs), source))
            self.current_tab = (len(self.tabs)-1, source)

        elif self.capabilities['browserName'] == 'firefox':

            self.current_tab += 1
            self.tabs.insert(self.current_tab, source)
            new_win = self.driver.window_handles[self.current_tab]
            self.driver.switch_to_window(new_win)

    def quit(self):
        """
        This method closes the current webdriver instance.
        """
        self.current_tab = {}
        self.tabs = []
        self.driver.quit()

    def scroll_to(self, selector):
        """
        This method can scroll the current browser
        window to the selected element.

        :param selector: The specified element to scroll to.
        :type selector: str.
        """
        position = str(self._search_element(selector).location['y'])
        self.driver.execute_script("window.scrollTo(0,%s);" % position)

    def scroll_to_bottom(self):
        """
        This method can scroll the current browser
        window to the bottom of the webpage.
        """
        self.driver.execute_script("""window.scrollTo(0,
                                    document.body.scrollHeight);""")

    def scroll_to_top(self):
        """
        This method can scroll the current browser
        window to the top of the webpage.
        """
        self.driver.execute_script("""window.scrollTo(0,
                                    document.body.scrollTop);""")

    def see_element(self, selector):
        """
        This method asserts the visible of an element to the user,
        except 'NoSuchElementException' is raised.

        :param selector: Element selector.
        :type selector: str.
        :returns: True if element is not visible.
        """
        try:
            assert self._search_element(selector).is_displayed()
        except NoSuchElementException:
            assert False

    def dont_see_element(self, selector):
        """
        This method asserts the visible of an element to the user,
        except 'NoSuchElementException' is raised.

        :param selector: Element selector.
        :type selector: str.
        :returns: True if element is not visible.
        """
        try:
            assert not self._search_element(selector).is_displayed()
        except NoSuchElementException:
            assert True

    def see_clickable_element(self, selector):
        """
        This method asserts if the element is clickable using 'is_enabled',
        except 'NoSuchElementException' is raised.

        :param selector: Element selector.
        :type selector: str.
        :returns: True if element is clickable.
        """
        try:
            assert self._search_element(selector).is_enabled()
        except NoSuchElementException:
            assert False

    def see_selected_element(self, selector):
        """
        This method asserts if the element is selected or checked (if checkbox),
        except 'NoSuchElementException' is raised.

        :param selector: Element selector.
        :type selector: str.
        :returns: True if element is selected or checked.
        """
        try:
            assert self._search_element(selector).is_selected()
        except NoSuchElementException:
            assert False

    def set_timeout(self, timeouts):
        """
        This method sets the amount of time that the script should wait during
        an execute_async_script call before throwing an error.

        :param timeouts: A dictionary containing the amount of time to wait
        (in seconds) and the script. example: {'page_load':x,'script':y}
        :type timeouts: dict.
        """
        if timeouts['page_load'] is not None:
            self.driver.set_page_load_timeout(timeouts['page_load'])
        if timeouts['script'] is not None:
            self.driver.set_script_timeout(timeouts['script'])

    def set_window_position(self, x, y):
        """
        This method sets the position of the browser window.

        :param x: The desired window x-axis position.
        :type x: str.
        :param y: The desired window y-axis position.
        :type y: str.
        """
        self.driver.set_window_position(x, y)

    def set_window_size(self, width, height):
        """
        This method sets the size of the browser window.

        :param width: The desired window width.
        :type width: str.
        :param height: The desired window height.
        :type height: str.
        """
        self.driver.set_window_size(width, height)

    def smart_wait(self, cond, timeout, value=None, msg='', default=True):
        """
        This method implements a smart wait using WebDriverWait.
        If 'default' is set to True, 'until' is used.
        It calls the 'condition' provided with the driver as an argument until
        the return value is not False.
        ________________________________________________________________
        If 'default' is set to False, 'until_not' is used.
        It calls the 'condition' provided with the driver as an argument until
        the return value is False.

        :param cond: The condition to be met for the wait to disengage.
        :type cond: str.
        :param timeout: The number of seconds before timeout.
        :type timeout: int.
        :param msg: The message to display while smart wait is active.
        :type msg: str.
        :param default: True for until, False for until_not methods.
        :type default: bool.
        """
        tmp_wait = WebDriverWait(self.driver, timeout)
        if default:
            tmp_wait.until(cond, msg)
        else:
            tmp_wait.until_not(cond, msg)

    def switch_to(self, source, item=1):
        """
        This method switches to a specified browser tab.
        :param source: The specified tab to switch to.
        :type source: str.
        """
        if self.capabilities['browserName'] == 'chrome':
            self.current_tab = list(filter(lambda x: source in x[1], self.tabs))[item - 1]
            sw_win = self.driver.window_handles[self.current_tab[0]]
            self.driver.switch_to_window(sw_win)
        elif self.capabilities['browserName'] == 'firefox':
            tabs_ind = enumerate(self.tabs)
            self.current_tab = list(filter(lambda x: source in x[1], tabs_ind))[item - 1][0]
            sw_win = self.driver.window_handles[self.current_tab]
            self.driver.switch_to_window(sw_win)

    def switch_to_next_tab(self):
        """
        This method switches to the next available browser tab.
        """
        if self.capabilities['browserName'] == 'chrome':
            next_t = self.tabs.index(self.current_tab) + 1
            self.current_tab = self.tabs[next_t]
            new_win = self.driver.window_handles[self.current_tab[0]]
            self.driver.switch_to_window(new_win)
        elif self.capabilities['browserName'] == 'firefox':
            self.current_tab += 1
            new_win = self.driver.window_handles[self.current_tab]
            self.driver.switch_to_window(new_win)

# Why don't we use CTRL+TAB or CTRL+SHIFT+TAB?
    def switch_to_previous_tab(self):
        """
        This method switches to the previous available browser tab.
        """
        if self.capabilities['browserName'] == 'chrome':
            previous = self.tabs.index(self.current_tab) - 1
            self.current_tab = self.tabs[previous]
            new_win = self.driver.window_handles[self.current_tab[0]]
            self.driver.switch_to_window(new_win)
        elif self.capabilities['browserName'] == 'firefox':
            self.current_tab -= 1
            new_win = self.driver.window_handles[self.current_tab]
            self.driver.switch_to_window(new_win)

    def submit_a_form(self, selector):
        """
        This method submits a form.

        :param selector: The element that is part of the form to submit.
        :type selector: str.
        """
        self._search_element(selector).submit()

    def refresh_page(self):
        """
        This method refreshes the current page.
        """
        self.driver.refresh()

    def resize_window(self, window_size):
        """
        This method resizes the browser window.

        Usage: I.resize_window(600X800)

        :param window_size: The requested resolution in ###X### format.
        :type window_size: str.
        """
        window_width, window_height = window_size.split('x')
        self.driver.set_window_size(window_width, window_height)

    def type_enter(self, selector):
        """
        This method sends an Enter (or Return) keystroke to the selected
        element.

        :param selector: The selected element to send the keystroke.
        :type selector: str.
        """
        self._search_element(selector).send_keys(Keys.ENTER)

    def take_a_screenshot(self, path):
        """
        This method saves a screenshot of the current page to a PNG image
        file. Use full paths in your filename.

        Usage: I.take_a_screenshot('/screenshots/page.png')

        :param path: The full path you wish to save your screenshot to. Should
        end with a .png extension. eg. 'screenshots/test1.png'
        :type path: str.
        """
        self.driver.save_screenshot(path)

    def take_a_screenshot_element(self, selector, path):
        """
        This method saves a screenshot of a selected element to a PNG image
        file. Use full paths in your filename.

        Usage: I.take_a_screenshot_element('/screenshots/element.png')

        :param path: The full path you wish to save your screenshot to. Should
        end with a .png extension. eg. '/screenshots/test1.png'
        :type path: str.
        """
        element = self._search_element(selector)
        element.screenshot(path)

    def wait(self, t):
        """
        This method waits or sleeps for a specified interval.

        :param t: Specified wait time.
        :type t: int.
        """
        time.sleep(t)

    def wait_for_element(self, selector, time):
        """
        This method asserts if the selected element is displayed, if not,
        it waits a specified interval.

        :param selector: Specified text source selector.
        :type selector: str.
        :param time: Specified wait time.
        :type time: int.
        """
        if self.see_element(selector) is not True:
            self.wait(time)

    def wait_for_enable(self, selector, time):
        """
        This method asserts if the selected element is enabled, if not,
        it waits a specified interval.

        :param selector: Specified text source selector.
        :type selector: str.
        :param time: Specified wait time.
        :type time: int.
        """

        if self.see_element_clickable(selector) is not True:
            self.wait(time)

    def wait_for_text(self, text, selector, time):
        """
        This method asserts if the selected text is equal to the specified
        text, if not, it waits a specified interval.

        :param text: Specified text.
        :type text: str.
        :param selector: Specified text source selector.
        :type selector: str.
        :param time: Specified wait time.
        :type time: int.
        """
        if self.get_text_from(selector) is not text:
            self.wait(time)

    def wait_url_equals(self, url, time):
        """
        This method asserts if the current url is the specified url, if not,
        it waits a specified interval and validates again.

        :param url: The target url.
        :type url: str.
        :param time: The time interval to wait for the url be tested.
        :type time: int.
        """
        current_url = self.driver.current_url
        if current_url != url:
            self.wait(time)
            self.wait_url_equals(url, time)

    def _search_element(self, full_selector):
        """
        This method can find an element using different selection tools.

        :param full_selector: key:value selector using method:selector format.
        key = css - Find element by CSS Selector.
        key = xpath - Find element by xpath.
        key = id - Find element by ID.
        key = name - Find element by Name.
        key = link - Find element by link text.
        key = plink - Find element by partial link text.
        key = tag - Find element by Tag Name.
        key = class - Find element by Class Name.

        :type selector: dict.
        :returns: The element if found in the DOM,
        else it raises NoSuchElementException.
        """
        key_selector = ""
        value_selector = ""
        dispatcher = {
            'css': self.driver.find_element_by_css_selector,
            'xpath': self.driver.find_element_by_xpath,
            'id': self.driver.find_element_by_id,
            'name': self.driver.find_element_by_name,
            'link': self.driver.find_element_by_link_text,
            'plink': self.driver.find_element_by_partial_link_text,
            'tag': self.driver.find_element_by_tag_name,
            'class': self.driver.find_element_by_class_name
        }
        if type(full_selector) is dict:
            key_selector = list(full_selector.keys())[0]
            value_selector = list(full_selector.values())[0]
            if key_selector in dispatcher.keys():
                try:
                    return dispatcher[key_selector](value_selector)
                except NoSuchElementException:
                    return None
        else:
            for selector in dispatcher.keys():
                try:
                    return dispatcher[selector](full_selector)
                except NoSuchElementException:
                    continue
        return None
