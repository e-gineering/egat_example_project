import egat.testset as testset
from egat.execution_groups import execution_group
from egat.shared_resource import SharedResource

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from test_helpers import authentication_helper
from test_helpers import browser_helper
from page_models.process_payment import ProcessPaymentPage
from page_models.payment import PaymentEdit, PaymentIndex
from page_models.order import OrderEdit

class OrdersListResource(SharedResource): pass

@execution_group("cms.order_manager.test_payment.TestPaymentProcessing")
class TestPaymentProcessing(testset.SequentialTestSet):
    @browser_helper.BrowserStartupResource.decorator
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment.get('browser', ''))
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['auth']['username'],
            self.configuration['auth']['password'],
        )

    def teardown(self):
        self.browser.quit()

    def test_open_payment_page(self):
        self.page = ProcessPaymentPage(self.browser, self.configuration['base_url'])
        self.page.open()

    @OrdersListResource.decorator
    def test_submit_payment(self):
        config = self.configuration['payment_tests']

        # Pick the first order in the select box
        orders = self.page.get_orders()
        assert len(orders) > 0, "Need at least 1 valid order to run tests."
        self.order_id = orders[0]['id']

        # Fill the form
        self.page.fill_form(
            order_id=self.order_id,
            card_type=config['card_type'],
            card_number=config['card_number'],
            exp_date=config['expiration_date'],
            ccv=config['ccv'],
        )

        # And submit
        self.page.submit_payment()

    def test_success_message(self):
        # Check the flash message
        WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located(
                (By.ID, "flash-message")
            )
        )
        message_element = self.browser.find_element_by_id("flash-message")
        assert message_element.text == self.configuration['payment_tests']['success_message']

    def test_order_status_changed(self):
        page = OrderEdit(self.browser, self.configuration['base_url'])
        page.open(self.order_id)
        fields = page.get_fields()
        assert fields['status'] == 2, "Order status was not changed to 'Payment Received'. %s" % fields['status']

    def test_payment_created(self):
        # Get the id of the order we created
        index_page = PaymentIndex(self.browser, self.configuration['base_url'])
        index_page.open()
        payment_id = index_page.id_for_payment(self.order_id)
        assert payment_id != None, "Could not find a Payment."

        # Check that the status is correct
        edit_page = PaymentEdit(self.browser, self.configuration['base_url'])
        edit_page.open(payment_id)
        payment = edit_page.get_fields()

        assert payment['status'] == 2, "Payment status is not 'Processed'"
