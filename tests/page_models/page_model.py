from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageModel():
    def __init__(self, browser, url):
        """"Takes a Selenium Webdriver object and instantiates the PageModel."""
        self.browser = browser
        self.url = url
        # Loads up page pointed to by 'self.url'
        self.open()

    def open(self):
        """Opens the page passed into the constructor as 'url'."""
        self.browser.get(self.url)

    def refresh(self):
        """Reloads the page passed into the constructor as 'url'."""
        self.open()

    def wait_for_text_to_load_in_element(self, css_selector, text_to_match_against, max_wait_in_seconds=20):
        """Uses 'css_selector' to find an element and then waits for that element's text to /
        be equivalent to 'text_to_match_against' for a max of 'max_wait_seconds'."""
        # Wait for page to load
        WebDriverWait(self.browser, max_wait_in_seconds).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, css_selector),
                text_to_match_against
            )
        )
