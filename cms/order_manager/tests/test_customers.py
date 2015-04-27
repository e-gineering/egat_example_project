import egat.testset as testset
from egat.shared_resource import SharedResource
from egat.execution_groups import execution_group
from test_helpers import authentication_helper
from test_helpers import browser_helper
from page_models.customer import CustomerIndex, CustomerCreate, CustomerEdit
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class CustomerCreationAndDeletionResource(SharedResource):
    """
    A SharedResource that represents creating or deleting an Order.
    """
    pass

@execution_group("cms.order_manager.test_customers.TestCustomers")
class TestCustomers(testset.SequentialTestSet):

    @browser_helper.BrowserStartupResource.decorator
    def setup(self):
        self.browser = browser_helper.get_browser(self.environment.get('browser', ''))
        authentication_helper.authenticate(
            self.browser,
            self.configuration['base_url'],
            self.configuration['auth']['username'],
            self.configuration['auth']['password'],
        )

    @CustomerCreationAndDeletionResource.decorator
    def testCreateCustomer(self):
        # Count the number of customers before creation.
        index_page = CustomerIndex(self.browser, self.configuration['base_url'])
        index_page.open()
        customers_before_creation = index_page.get_customer_elements()

        # Fill the form and submit it
        create_page = CustomerCreate(self.browser, self.configuration['base_url'])
        create_page.open()
        first_name = self.configuration['customer_tests']['first_name']
        last_name = self.configuration['customer_tests']['last_name']
        create_page.fill_form(first_name, last_name)
        create_page.submit_form()

        # Verify that customer was created
        customers_after_creation = index_page.get_customer_elements()
        assert len(customers_after_creation) == len(customers_before_creation) + 1, \
            "Could not find created customer."

        customer_pattern = "([0-9]+) %s %s" % (first_name, last_name)
        match = re.match(customer_pattern, customers_after_creation[0].text)
        assert match is not None, "Could not find created customer."

        self.customer_id = index_page.id_for_customer_named(first_name, last_name)

    def testEditCustomer(self):
        alt_first_name = self.configuration['customer_tests']['alt_first_name']

        # Edit the customer's first name
        edit_page = CustomerEdit(self.browser, self.configuration['base_url'])
        edit_page.open(self.customer_id)
        edit_page.change_fields(first_name=alt_first_name)
        edit_page.save_changes()

        # Verify that the customer's first name was changed
        edit_page.open(self.customer_id)
        fields = edit_page.get_fields()
        assert fields['first_name'] == alt_first_name, \
            "Could not verify that customer was edited."


    @CustomerCreationAndDeletionResource.decorator
    def testDeleteCustomer(self):
        # Count the number of customers before creation.
        index_page = CustomerIndex(self.browser, self.configuration['base_url'])
        index_page.open()
        customers_before_deletion = index_page.get_customer_elements()

        # Delete the customer
        edit_page = CustomerEdit(self.browser, self.configuration['base_url'])
        edit_page.open(self.customer_id)
        edit_page.delete_customer()

        # Wait for index page to load
        WebDriverWait(self.browser, 20).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "div#content > h1"),
                "Select customer to change"
            )
        )

        # Verify that the customer is gone from the index page
        customers_after_deletion = index_page.get_customer_elements()
        assert len(customers_after_deletion) == len(customers_before_deletion) - 1, \
            "Could not verify that customer was deleted."

    def teardown(self):
        self.browser.quit()
