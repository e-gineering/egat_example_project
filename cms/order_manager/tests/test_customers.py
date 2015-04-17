import egat.testset as testset
from test_helpers import authentication_helper
from test_helpers import browser_helper


class TestCustomers(testset.SequentialTestSet):
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment.get('browser', ''))
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['username'],
            self.configuration['password'],
        )

    def testCreateOrder(self):
        self.browser.get('http://localhost:8000/admin/order_manager/order/')
        # Click the 'add' button
        self.browser.find_element_by_css_selector('a[class="addlink"]').click()

        # Fill out the form


    def teardown(self):
        self.browser.quit()