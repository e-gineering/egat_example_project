from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from egat.shared_resource import SharedResource


class BrowserStartupResource(SharedResource):
    """
    A Shared Resource that represents the opening of a browser. Various browsers on
    various platforms have trouble starting up multiple instances of themselves
    simultaneously.
    """
    pass


class InvalidBrowserException(Exception):
    pass


def get_browser(environment):
    if environment.get('browser_location', '') == "browserstack":
        desired_cap = {'browserstack.local': True,
                       'os': environment.get('os', ''),
                       'os_version': environment.get('os_version', ''),
                       'browser': environment.get('browser', ''),
                       'browser_version': environment.get('browser_version', '')
        }

        return webdriver.Remote(
            command_executor="http://" + environment.get('userName', '') + ":" + environment.get('key', '') + "@hub.browserstack.com:80/wd/hub",
            desired_capabilities=desired_cap)

    elif environment.get('browser_location', '') == "local":

        """Takes a browser name and returns an instance of that browser as a
        Selenium Webdriver object. Valid strings are 'Firefox', 'Chrome', 'IE', 'Opera',
        and 'PhantomJS'. An invalid string will result in a Firefox browser being
        returned."""
        if environment.get('browser', '') == "Firefox":
            return webdriver.Firefox()
        elif environment.get('browser', '') == "Chrome":
            return webdriver.Chrome()
        elif environment.get('browser', '') == "IE":
            return webdriver.Ie()
        elif environment.get('browser', '') == "Opera":
            return webdriver.Opera()
        elif environment.get('browser', '') == "PhantomJS":
            return webdriver.PhantomJS()
        elif environment.get('browser', '') == "Safari":
            return webdriver.Safari
        else:
            return webdriver.Firefox()
