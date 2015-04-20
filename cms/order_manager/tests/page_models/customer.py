from page_models.page_model import PageModel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class CustomerIndex(PageModel):
    def open(self):
        """Opens the Customer page."""
        self.browser.get(self.base_url + "/admin/order_manager/customer/")

    def get_customer_elements(self):
        """Returns a list of all the customer <a> elements on the page."""
        return self.browser.find_elements_by_css_selector("th[class~='field-__str__'] > a")

    def id_for_customer_named(self, first_name, last_name):
        """Takes a first and last name and returns the id of the first customer
        found with that first and last name. Returns None if no customer is found."""
        customer_regex = "([0-9]+) %s %s" % (first_name, last_name)
        for customer_element in self.get_customer_elements():
            match = re.match(customer_regex, customer_element.text)
            if match:
                return int(match.group(1))

class CustomerCreate(PageModel):
    def open(self):
        """Opens the Add Customer page."""
        self.browser.get(self.base_url + "/admin/order_manager/customer/add/")

    def fill_form(self, first_name, last_name):
        """Takes a first and last name and fills out the Customer form."""
        # Find the input elements
        first_name_box = self.browser.find_element_by_css_selector("input#id_first_name")
        last_name_box = self.browser.find_element_by_css_selector("input#id_last_name")

        first_name_box.send_keys(first_name)
        last_name_box.send_keys(last_name)

    def submit_form(self):
        self.browser.find_element_by_css_selector("input[name='_save']").click()

class CustomerEdit(PageModel):
    def open(self, customer_id):
        """Takes a customer id (as an int) and opens the "Change customer" page for that customer."""
        self.browser.get("%s/admin/order_manager/customer/%d" % (self.base_url, customer_id))

    def change_fields(self, first_name=None, last_name=None):
        """Takes variables that correspond to the fields on a Customer and changes
        the existing values to the given ones. All fields that are not passed to
        this function will be left alone."""
        if first_name is not None:
            first_name_box = self.browser.find_element_by_css_selector("input#id_first_name")
            first_name_box.clear()
            first_name_box.send_keys(first_name)
        if last_name is not None:
            last_name_box = self.browser.find_element_by_css_selector("input#id_last_name")
            last_name_box.clear()
            last_name_box.send_keys(last_name)

    def get_fields(self):
        """Gets the values in the customer fields and returns them in a dictionary."""
        return {
            'first_name': self.browser.find_element_by_css_selector("input#id_first_name").get_attribute('value'),
            'last_name': self.browser.find_element_by_css_selector("input#id_last_name").get_attribute('value'),
        }

    def save_changes(self):
        """Clicks the 'save' button to save any changes made to this Customer."""
        self.browser.find_element_by_css_selector("input[name='_save']").click()

    def delete_customer(self):
        """Clicks the 'delete' button and walks through the confirmation to delete
        the current Customer."""
        # Click the delete button
        self.browser.find_element_by_link_text("Delete").click()
        # Wait for the confirmation page
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Are you sure?')]")
            )
        )
        # Click the confirmation button
        self.browser.find_element_by_css_selector("input[type='submit']").click()
