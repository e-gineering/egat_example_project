import egat.testset as testset
from egat.execution_groups import execution_group
from test_helpers import authentication_helper
from test_helpers import browser_helper
from page_models.order import OrderIndex, OrderCreate, OrderEdit
import re

@execution_group("cms.order_manager.test_orders.TestOrders")
class TestOrders(testset.SequentialTestSet):
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment.get('browser', ''))
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['auth']['username'],
            self.configuration['auth']['password'],
        )

    def testCreateOrder(self):
        status = self.configuration['order_tests']['status']
        customer_name = self.configuration['order_tests']['customer_name']
        product_id = self.configuration['order_tests']['product_id']
        product_name = self.configuration['order_tests']['product_name']
        quantity = self.configuration['order_tests']['quantity']

        # Fill the form and submit it
        create_page = OrderCreate(self.browser, self.configuration['base_url'])
        create_page.open()
        create_page.fill_form(product_id, product_id, quantity, status)
        create_page.submit_form()

        # Verify that order was created
        index_page = OrderIndex(self.browser, self.configuration['base_url'])
        orders = index_page.get_order_elements()
        order_pattern = "%d %s for %s" % (quantity, product_name, customer_name)
        order_matcher = lambda e: re.match(order_pattern, e.text)
        assert(len(filter(order_matcher, orders)) == 1)

    def testEditOrder(self):
        customer_name = self.configuration['order_tests']['customer_name']
        product_name = self.configuration['order_tests']['product_name']
        quantity = self.configuration['order_tests']['quantity']
        alt_quantity = self.configuration['order_tests']['alt_quantity']

        # Get the id of our order
        index_page = OrderIndex(self.browser, self.configuration['base_url'])
        order_id = index_page.id_for_order(quantity, product_name, customer_name)

        # Edit the order's first name
        edit_page = OrderEdit(self.browser, self.configuration['base_url'])
        edit_page.open(order_id)
        edit_page.change_fields(quantity=alt_quantity)
        edit_page.save_changes()

        # Verify that the order's first name was changed
        index_page = OrderIndex(self.browser, self.configuration['base_url'])
        orders = index_page.get_order_elements()

        # Old order should be gone
        old_order_pattern = "%d %s for %s" % (quantity, product_name, customer_name)
        old_order_matcher = lambda e: re.match(old_order_pattern, e.text)
        assert(len(filter(old_order_matcher, orders)) == 0)

        # New order should be present
        new_order_pattern = "%d %s for %s" % (alt_quantity, product_name, customer_name)
        new_order_matcher = lambda e: re.match(new_order_pattern, e.text)
        assert(len(filter(new_order_matcher, orders)) == 1)

    def testDeleteOrder(self):
        customer_name = self.configuration['order_tests']['customer_name']
        product_name = self.configuration['order_tests']['product_name']
        alt_quantity = self.configuration['order_tests']['alt_quantity']

        # Get the id of our order
        index_page = OrderIndex(self.browser, self.configuration['base_url'])
        order_id = index_page.id_for_order(alt_quantity, product_name, customer_name)

        # Delete the order
        edit_page = OrderEdit(self.browser, self.configuration['base_url'])
        edit_page.open(order_id)
        edit_page.delete_order()

        # Verify that the order is gone from the index page
        order_pattern = "%d %s for %s" % (alt_quantity, product_name, customer_name)
        order_matcher = lambda e: re.match(order_pattern, e.text)
        assert(len(filter(order_matcher, index_page.get_order_elements())) == 0)

    def teardown(self):
        self.browser.quit()
