from selenium import webdriver

class InvalidBrowserException(Exception):
    pass

def get_browser(browser_name):
    """Takes a string browser name and returns an instance of that browser as a
    Selenium Webdriver object. Valid strings are 'Firefox', 'Chrome', 'IE', 'Opera',
    and 'PhantomJS'. An invalid string will result in a Firefox browser being
    returned."""
    if browser_name == "Firefox":
        return webdriver.Firefox()
    elif browser_name == "Chrome":
        return webdriver.Chrome()
    elif browser_name == "IE":
        return webdriver.Ie()
    elif browser_name == "Opera":
        return webdriver.Opera()
    elif browser_name == "PhantomJS":
        return webdriver.PhantomJS()
    else:
        return webdriver.Firefox()
