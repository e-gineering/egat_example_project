import egat.testset as testset
from egat.execution_groups import execution_group
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_helpers import browser_helper

@execution_group("cms.order_manager.tests.test_login.TestLogin")
class TestLogin(testset.SequentialTestSet):
    USERNAME_SELECTOR = "input[name='username']"
    PASSWORD_SELECTOR = "input[name='password']"
    SUBMIT_SELECTOR = "input[type='submit']"

    def setup(self):
        # Instantiate the browser based on the 'browser' environment variable
        browser_type = self.environment.get('browser', '')
        self.browser = browser_helper.get_browser(browser_type)

    def teardown(self):
        self.browser.quit()

    def testOpenLoginPage(self):
        """
        Opens the Login page and verifies that the correct elements are present
        """
        self.browser.get(self.configuration['base_url'] + "/login/")
        self.verify_login_page()

    def testLoginAction(self):
        """
        Logs in as the default user and verifies redirection to the Django administration page.
        """
        if self.environment['browser'] == "Chrome":
            assert(False)
        username_input = self.browser.find_element_by_css_selector(self.USERNAME_SELECTOR)
        password_input = self.browser.find_element_by_css_selector(self.PASSWORD_SELECTOR)
        submit_button = self.browser.find_element_by_css_selector(self.SUBMIT_SELECTOR)

        username_input.send_keys(self.configuration['username'])
        password_input.send_keys(self.configuration['password'])
        submit_button.click()

        WebDriverWait(self.browser, 20).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "div#user-tools > strong"),
                self.configuration['username']
            )
        )

    def testLogoutAction(self):
        """
        Logs the user out and verifies that the logout page is shown
        """

        self.browser.find_element_by_link_text("Log out").click()
        WebDriverWait(self.browser, 20).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "div#content > h1"),
                "Logged out"
            )
        )

    def testLoggedOut(self):
        """"
        Verifies that internal pages redirect to the login page
        """
        self.browser.get(self.configuration['base_url'])
        self.verify_login_page()

    def verify_login_page(self):
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.USERNAME_SELECTOR)
            )
        )
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.PASSWORD_SELECTOR)
            )
        )
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.SUBMIT_SELECTOR)
            )
        )
