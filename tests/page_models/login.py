from page_model import PageModel


class LoginIndex(PageModel):
    def fill_login_form(self, username, password):
        username_css_selector = "input[name='username']"
        password_css_selector = "input[name='password']"
        username_input = self.browser.find_element_by_css_selector(username_css_selector)
        password_input = self.browser.find_element_by_css_selector(password_css_selector)
        username_input.send_keys(username)
        password_input.send_keys(password)

    def submit_login_form(self):
        submit_button_css_selector = "input[type='submit']"
        submit_button = self.browser.find_element_by_css_selector(submit_button_css_selector)
        submit_button.click()

    def logout(self):
        self.browser.find_element_by_link_text("LOG OUT").click()
