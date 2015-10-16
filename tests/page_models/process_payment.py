from page_models.page_model import PageModel
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


class ProcessPaymentPage(PageModel):
    ORDER_SELECT_SELECTOR = "select[name='order_id']"

    def get_orders(self):
        """Returns a list of dictionaries representing the choices in the Order
        select box. Dictionaries will be of the form:
            {
                "id": int,
                "name": str,
            }
        """
        try:
            select = Select(self.browser.find_element_by_css_selector(self.ORDER_SELECT_SELECTOR))
            dict_extractor = lambda o: {'id': o.get_attribute('value'), 'name': o.text}
            return map(dict_extractor, select.options)
        except NoSuchElementException:
            # If element cannot be found, return an empty dictionary.
            return dict()

    def fill_form(self, order_id=None, card_type=None,
                  card_number=None, exp_date=None, ccv=None):
        """
        Fills out the Payment Processing Form. Any form fields corresponding to
        ommitted parameters will not be changed.

        :param order_id: The id of the Order you wish to select.
        :param card_type: The string of the type you wish to choose from the 'card_type' select box. Use the visible text of the Card Type you want, not the HTML value of the <option> tag.
        :param card_number: The string you wish to insert into the Card Number field.
        :param exp_date: The string you wish to insert into the Expiration Date field.
        :param ccv: The string you wish to insert into the CCV field.
        """
        if order_id:
            order_select = Select(self.browser.find_element_by_css_selector(self.ORDER_SELECT_SELECTOR))
            order_select.select_by_value(order_id)
        if card_type:
            card_type_select = Select(self.browser.find_element_by_css_selector("select[name='card_type']"))
            card_type_select.select_by_value(card_type)
        if card_number:
            card_number_input = self.browser.find_element_by_css_selector("input[name='card_number']")
            card_number_input.clear()
            card_number_input.send_keys(card_number)
        if exp_date:
            exp_date_input = self.browser.find_element_by_css_selector("input[name='expiration']")
            exp_date_input.clear()
            exp_date_input.send_keys(exp_date)
        if ccv:
            ccv_input = self.browser.find_element_by_css_selector("input[name='ccv']")
            ccv_input.clear()
            ccv_input.send_keys(ccv)

    def submit_payment(self):
        """Clicks the 'submit_payment' button."""
        self.browser.find_element_by_css_selector("input[type='submit']").click()

    def get_flash_message(self):
        """Gets the flash message from the top of the page."""
        return self.browser.find_element_by_css_selector("span#flash-message").text
