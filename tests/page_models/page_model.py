class PageModel():
    def __init__(self, browser, base_url):
        """"Takes a Selenium Webdriver object and instantiates the PageModel."""
        self.browser = browser
        self.base_url = base_url
