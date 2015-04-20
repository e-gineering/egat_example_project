import egat.testset as testset
from egat.execution_groups import execution_group
from test_helpers import authentication_helper
from test_helpers import browser_helper
from page_models.customer import CustomerIndex, CustomerCreate, CustomerEdit
import re

@execution_group("cms.order_manager.test_customers.TestCustomers")
class TestCustomers(testset.SequentialTestSet):
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment.get('browser', ''))
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['auth']['username'],
            self.configuration['auth']['password'],
        )

    def testCreateCustomer(self):
        # Fill the form and submit it
        create_page = CustomerCreate(self.browser, self.configuration['base_url'])
        create_page.open()
        first_name = self.configuration['customer_tests']['first_name']
        last_name = self.configuration['customer_tests']['last_name']
        create_page.fill_form(first_name, last_name)
        create_page.submit_form()

        # Verify that customer was created
        index_page = CustomerIndex(self.browser, self.configuration['base_url'])
        customers = index_page.get_customer_elements()
        customer_pattern = "([0-9]+) %s %s" % (first_name, last_name)
        customer_matcher = lambda e: re.match(customer_pattern, e.text)
        assert(len(filter(customer_matcher, customers)) == 1)

    def testEditCustomer(self):
        first_name = self.configuration['customer_tests']['first_name']
        last_name = self.configuration['customer_tests']['last_name']
        alt_first_name = self.configuration['customer_tests']['alt_first_name']

        # Get the id of our customer
        index_page = CustomerIndex(self.browser, self.configuration['base_url'])
        cust_id = index_page.id_for_customer_named(first_name, last_name)

        # Edit the customer's first name
        edit_page = CustomerEdit(self.browser, self.configuration['base_url'])
        edit_page.open(cust_id)
        edit_page.change_fields(first_name=alt_first_name)
        edit_page.save_changes()

        # Verify that the customer's first name was changed
        index_page = CustomerIndex(self.browser, self.configuration['base_url'])
        customers = index_page.get_customer_elements()

        # Old name should be gone
        old_customer_pattern = "([0-9]+) %s %s" % (first_name, last_name)
        old_customer_matcher = lambda e: re.match(old_customer_pattern, e.text)
        assert(len(filter(old_customer_matcher, customers)) == 0)

        # New name should be present
        new_customer_pattern = "([0-9]+) %s %s" % (alt_first_name, last_name)
        new_customer_matcher = lambda e: re.match(new_customer_pattern, e.text)
        assert(len(filter(new_customer_matcher, customers)) == 1)

    def testDeleteCustomer(self):
        alt_first_name = self.configuration['customer_tests']['alt_first_name']
        last_name = self.configuration['customer_tests']['last_name']

        # Get the id of our customer
        index_page = CustomerIndex(self.browser, self.configuration['base_url'])
        cust_id = index_page.id_for_customer_named(alt_first_name, last_name)

        # Delete the customer
        edit_page = CustomerEdit(self.browser, self.configuration['base_url'])
        edit_page.open(cust_id)
        edit_page.delete_customer()

        # Verify that the customer is gone from the index page
        customer_pattern = "%d %s %s" % (cust_id, alt_first_name, last_name)
        customer_matcher = lambda e: re.match(customer_pattern, e.text)
        assert(len(filter(customer_matcher, index_page.get_customer_elements())) == 0)

    def teardown(self):
        self.browser.quit()