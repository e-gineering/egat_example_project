import egat.testset as testset
from egat.shared_resource import SharedResource
from egat.execution_groups import execution_group
from test_helpers import authentication_helper
from test_helpers import browser_helper
from page_models.customer import CustomerIndex, CustomerCreate, CustomerEdit
import re

class CustomerListResource(SharedResource):
    """
    A SharedResource that represents anything that adds or removes items from the list
    of Customers.
    """
    pass


@execution_group("cms.order_manager.test_customers.TestCustomers")
class TestCustomers(testset.SequentialTestSet):

    @browser_helper.BrowserStartupResource.decorator
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment)
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['auth']['username'],
            self.configuration['auth']['password'],
        )

    @CustomerListResource.decorator
    def testCreateCustomer(self):
        # Count the number of customers before creation.
        target_url = self.configuration['base_url'] + "/admin/order_manager/customer/"
        index_page = CustomerIndex(self.browser, target_url)

        num_customers_before_creation = index_page.count_customers()

        # Fill the form and submit it
        target_url = self.configuration['base_url'] + "/admin/order_manager/customer/add/"
        create_page = CustomerCreate(self.browser, target_url)
        first_name = self.configuration['customer_tests']['first_name']
        last_name = self.configuration['customer_tests']['last_name']
        create_page.fill_form(first_name, last_name)
        create_page.submit_form()

        # Verify that customer was created
        num_customers_after_creation = index_page.count_customers()
        self.validate((num_customers_after_creation == num_customers_before_creation + 1),
                      error_message="Could not find created customer.")

        customer_pattern = "([0-9]+) %s %s" % (first_name, last_name)
        customers_after_creation = index_page.get_customer_elements()
        # Regular expression match
        match = re.match(customer_pattern, customers_after_creation[0].text)
        self.validate((match is not None), error_message="Could not find created customer.")

        self.customer_id = index_page.id_for_customer_named(first_name, last_name)

    def testEditCustomer(self):
        alt_first_name = self.configuration['customer_tests']['alt_first_name']

        # Edit the customer's first name
        target_url = "%s/admin/order_manager/customer/%d" % (self.configuration['base_url'],
                                                             self.customer_id)
        edit_page = CustomerEdit(self.browser, target_url)
        edit_page.change_input_field_by_id(field_id='id_first_name', new_value=alt_first_name)
        edit_page.save_changes()

        # Verify that the customer's first name was changed
        edit_page.refresh()
        first_name = edit_page.get_input_field_by_id('id_first_name')
        self.validate((first_name == alt_first_name),
                      error_message="Could not verify that customer was edited.")

    @CustomerListResource.decorator
    def testDeleteCustomer(self):
        # Count the number of customers before creation.
        target_url = self.configuration['base_url'] + "/admin/order_manager/customer/"
        index_page = CustomerIndex(self.browser, target_url)

        num_customers_before_deletion = index_page.count_customers()

        # Delete the customer
        target_url = "%s/admin/order_manager/customer/%d" % (self.configuration['base_url'],
                                                             self.customer_id)
        edit_page = CustomerEdit(self.browser, target_url)
        edit_page.delete_customer()

        edit_page.wait_for_text_to_load_in_element(css_selector="div#content > h1",
                                                   text_to_wait_for="Select customer to change")

        # Verify that the customer is gone from the index page
        num_customers_after_deletion = index_page.count_customers()
        self.validate((num_customers_after_deletion == num_customers_before_deletion - 1),
                      error_message="Could not verify that customer was deleted.")

    def teardown(self):
        self.browser.quit()
