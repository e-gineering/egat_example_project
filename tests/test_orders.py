import egat.testset as testset
from egat.shared_resource import SharedResource
from egat.execution_groups import execution_group
from test_helpers import authentication_helper
from test_helpers import browser_helper
from page_models.order import OrderIndex, OrderCreate, OrderEdit
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderListResource(SharedResource):
    """
    A SharedResource that represents anything that adds or removes items from the list
    of Orders.
    """
    pass

@execution_group("cms.order_manager.test_orders.TestOrders")
class TestOrders(testset.SequentialTestSet):
    @browser_helper.BrowserStartupResource.decorator
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment.get('browser', ''))
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['auth']['username'],
            self.configuration['auth']['password'],
        )

    @OrderListResource.decorator
    def testCreateOrder(self):
        status = self.configuration['order_tests']['status']
        customer_name = self.configuration['order_tests']['customer_name']
        product_id = self.configuration['order_tests']['product_id']
        product_name = self.configuration['order_tests']['product_name']
        quantity = self.configuration['order_tests']['quantity']

        # Count the number of orders before order creation
        target_url = self.configuration['base_url'] + "/admin/order_manager/order/"
        index_page = OrderIndex(self.browser, target_url)
        orders_before_creation = index_page.get_order_elements()

        # Fill the form and submit it
        target_url = self.configuration['base_url'] + "/admin/order_manager/order/add/"
        create_page = OrderCreate(self.browser, target_url)
        create_page.fill_form(product_id, product_id, quantity, status)
        create_page.submit_form()

        # Verify that a new order was created
        orders_after_creation = index_page.get_order_elements()
        assert len(orders_after_creation) == len(orders_before_creation) + 1, \
            "Could not find created order on index page."
        assert orders_after_creation[0].text == "%d %s for %s" % (quantity, product_name, customer_name), \
            "Could not find created order on index page."

        self.order_id = index_page.id_for_order(quantity, product_name, customer_name)

    def testEditOrder(self):
        alt_quantity = self.configuration['order_tests']['alt_quantity']

        # Edit the order's first name
        target_url = "%s/admin/order_manager/order/%s" % (self.configuration['base_url'], self.order_id)
        edit_page = OrderEdit(self.browser, target_url)
        edit_page.change_fields(quantity=alt_quantity)
        edit_page.save_changes()

        # Verify that the changes were saved
        edit_page.refresh()
        fields = edit_page.get_fields()
        assert fields['quantity'] == alt_quantity, "Edit was not successfully saved."

    @OrderListResource.decorator
    def testDeleteOrder(self):
        # Get a count of the orders before the deletion
        target_url = self.configuration['base_url'] + "/admin/order_manager/order/"
        index_page = OrderIndex(self.browser, target_url)
        orders_before_deletion = index_page.get_order_elements()

        # Delete the order
        target_url = "%s/admin/order_manager/order/%s" % (self.configuration['base_url'], self.order_id)
        edit_page = OrderEdit(self.browser, target_url)
        edit_page.delete_order()

        # Wait for index page to load
        WebDriverWait(self.browser, 20).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "div#content > h1"),
                "Select order to change"
            )
        )

        # Verify that the order is gone from the index page
        assert len(index_page.get_order_elements()) == len(orders_before_deletion) - 1, \
            "Could not verify that order was deleted."

    def teardown(self):
        self.browser.quit()
