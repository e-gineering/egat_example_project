import egat.testset as testset
from egat.execution_groups import execution_group
from egat.shared_resource import SharedResource
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
        target_url = self.configuration['base_url'] + "/order_manager/process_payment/"
        self.page = ProcessPaymentPage(self.browser, target_url)

    @OrdersListResource.decorator
    def test_submit_payment(self):
        config = self.configuration['payment_tests']

        # Pick the first order in the select box
        orders = self.page.get_orders()
        self.validate((len(orders) > 0),
                      error_message="Need at least 1 valid order to run tests.")
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
        self.page.wait_for_presence_of_element(element_id="flash-message", max_wait_in_seconds=15)
        message_element = self.browser.find_element_by_id("flash-message")
        self.validate(message_element.text == self.configuration['payment_tests']['success_message'])

    def test_order_status_changed(self):
        target_url = "%s/admin/order_manager/order/%s" % (self.configuration['base_url'], self.order_id)
        order_edit_page = OrderEdit(self.browser, target_url)
        order_fields = order_edit_page.get_fields()
        self.validate((order_fields['status'] == 2),
                      error_message="Order status was not changed to 'Payment Received'. %s" % order_fields['status'])

    def test_payment_created(self):
        # Get the id of the order we created
        target_url = self.configuration['base_url'] + "/admin/order_manager/payment/"
        index_page = PaymentIndex(self.browser, target_url)
        payment_id = index_page.id_for_payment(self.order_id)
        self.validate((payment_id is not None),
                      error_message="Could not find a Payment.")

        # Check that the status is correct
        target_url = "%s/admin/order_manager/payment/%s" % (self.configuration['base_url'], payment_id)
        edit_page = PaymentEdit(self.browser, target_url)
        payment_fields = edit_page.get_fields()
        self.validate((payment_fields['status'] == 2),
                      error_message="Payment status is not 'Processed'")
