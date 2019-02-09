import egat.testset as testset
from egat.execution_groups import execution_group
from test_helpers import browser_helper
from page_models.login import LoginIndex


@execution_group("cms.order_manager.tests.test_login.TestLogin")
class TestLogin(testset.SequentialTestSet):
    @browser_helper.BrowserStartupResource.decorator
    def setup(self):
        # Instantiate the browser based on the 'browser' environment variable
        self.browser = browser_helper.get_browser(self.environment)

    def teardown(self):
        self.browser.quit()

    def testOpenLoginPage(self):
        """
        Opens the Login page and verifies that the correct elements are present
        """
        target_url = self.configuration['base_url'] + "/admin/login/"
        self.index_page = LoginIndex(self.browser, target_url)
        self.verify_login_page(self.index_page)

    def testLoginAction(self):
        """
        Logs in as the default user and verifies redirection to the Django administration page.
        """
        self.index_page.fill_login_form(self.configuration['auth']['username'], self.configuration['auth']['password'])
        self.index_page.submit_login_form()
        self.index_page.wait_for_text_to_load_in_element(css_selector="div#user-tools > strong",
                                                         text_to_wait_for=self.configuration['auth']['username'])

    def testLogoutAction(self):
        """
        Logs the user out and verifies that the logout page is shown
        """
        self.index_page.logout()
        self.index_page.wait_for_text_to_load_in_element(css_selector="div#content > h1",
                                                         text_to_wait_for="Logged out")

    def testLoggedOut(self):
        """"
        Verifies that internal pages redirect to the login page
        """
        target_url = self.configuration['base_url'] + "/admin"
        login_page = LoginIndex(self.browser, target_url)
        self.verify_login_page(login_page)

    def verify_login_page(self, login_page):
        login_page.wait_for_presence_of_element_by_css(css_selector="input[name='username']")
        login_page.wait_for_presence_of_element_by_css(css_selector="input[name='password']")
        login_page.wait_for_presence_of_element_by_css(css_selector="input[type='submit']")
