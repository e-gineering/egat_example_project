from page_models.page_model import PageModel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from test_helpers.selenium_helper import get_selected_option
import re

class OrderIndex(PageModel):
    def open(self):
        """Opens the Order page."""
        self.browser.get(self.base_url + "/admin/order_manager/order/")

    def get_order_elements(self):
        """Returns a list of all the order <a> elements on the page."""
        return self.browser.find_elements_by_css_selector("th[class~='field-__str__'] > a")

    def id_for_order(self, quantity, product_name, last_name):
        """Takes a product name and a customer last name and returns the id of the
        first order found matching those parameters. Returns None if no order is
        found."""
        order_regex = "%d %s for %s" % (quantity, product_name, last_name)
        for order_element in self.get_order_elements():
            match = re.match(order_regex, order_element.text)
            if match:
                id_extractor = ".*/admin/order_manager/order/([0-9]+)/"
                id_match = re.match(id_extractor, order_element.get_attribute("href"))
                return int(id_match.group(1))

class OrderCreate(PageModel):
    def open(self):
        """Opens the Add Order page."""
        self.browser.get(self.base_url + "/admin/order_manager/order/add/")

    def fill_form(self, customer_id, product_id, quantity, status_text=None):
        """Takes a customer id, a product id, and a quantity, and fills out the Order form."""
        # Find the input elements
        customer_select = Select(self.browser.find_element_by_css_selector("select#id_customer"))
        product_select = Select(self.browser.find_element_by_css_selector("select#id_product"))
        quantity_box = self.browser.find_element_by_css_selector("input#id_quantity")
        status_select = Select(self.browser.find_element_by_css_selector("select#id_status"))

        customer_select.select_by_value(str(customer_id))
        product_select.select_by_value(str(product_id))
        quantity_box.clear()
        quantity_box.send_keys(str(quantity))
        if status_text:
            status_select.select_by_visible_text(status_text)

    def submit_form(self):
        self.browser.find_element_by_css_selector("input[name='_save']").click()

class OrderEdit(PageModel):
    def open(self, order_id):
        """Takes a order id (as an int) and opens the "Change order" page for that order."""
        self.browser.get("%s/admin/order_manager/order/%s" % (self.base_url, order_id))

    def get_fields(self):
        """Gets the values in the order's fields and returns them in a dictionary."""
        return {
            'status': int(get_selected_option(self.browser, "select#id_status")),
            'customer_id': int(get_selected_option(self.browser, "select#id_customer")),
            'product_id': int(get_selected_option(self.browser, "select#id_product")),
            'quantity': self.browser.find_element_by_css_selector("input#id_quantity").get_attribute('value'),
        }

    def change_fields(self, customer_id=None, product_id=None, quantity=None):
        """Takes variables that correspond to the fields on a Order and changes
        the existing values to the given ones. All fields that are not passed to
        this function will be left alone."""
        if customer_id is not None:
            customer_select = Select(self.browser.find_element_by_css_selector("select#id_customer"))
            customer_select.select_by_value(str(customer_id))
        if product_id is not None:
            product_select = Select(self.browser.find_element_by_css_selector("select#id_product"))
            product_select.select_by_value(str(product_id))
        if quantity is not None:
            quantity_box = self.browser.find_element_by_css_selector("input#id_quantity")
            quantity_box.clear()
            quantity_box.send_keys(str(quantity))

    def save_changes(self):
        """Clicks the 'save' button to save any changes made to this Order."""
        self.browser.find_element_by_css_selector("input[name='_save']").click()

    def delete_order(self):
        """Clicks the 'delete' button and walks through the confirmation to delete
        the current Order."""
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
