from page_model import PageModel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_helpers.selenium_helper import get_selected_option
import re


class PaymentIndex(PageModel):
    def get_payment_elements(self):
        """Returns a list of all the payment <a> elements on the page."""
        return self.browser.find_elements_by_css_selector("th[class~='field-__str__'] > a")

    def id_for_payment(self, order_id):
        """Takes an order_id and returns the id of the first payment with that
        order id. Returns None if no order is found."""
        payment_regex = "Order %s .*" % (order_id)
        for payment_element in self.get_payment_elements():
            match = re.match(payment_regex, payment_element.text)
            if match:
                id_extractor = ".*/admin/order_manager/payment/([0-9]+)/"
                id_match = re.match(id_extractor, payment_element.get_attribute("href"))
                return int(id_match.group(1))


class PaymentEdit(PageModel):
    def get_fields(self):
        """Gets the values in the payment fields and returns them in a dictionary."""

        return {
            'status': int(get_selected_option(self.browser, "select#id_status")),
            'order': int(get_selected_option(self.browser, "select#id_order")),
            'card_type': get_selected_option(self.browser, "select#id_card_type"),
            'card_number': self.browser.find_element_by_css_selector("input#id_card_number").get_attribute("value"),
            'expiration_date': self.browser.find_element_by_css_selector("input#id_expiration_date").get_attribute(
                "value"),
            'ccv': self.browser.find_element_by_css_selector("input#id_ccv").get_attribute("value"),
        }

    def save_changes(self):
        """Clicks the 'save' button to save any changes made to this Customer."""
        self.browser.find_element_by_css_selector("input[name='_save']").click()

    def delete_payment(self):
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
