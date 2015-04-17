def authenticate(browser, base_url, username, password):
    """Opens the login page and logs in with the given username and password."""
    USERNAME_SELECTOR = "input[name='username']"
    PASSWORD_SELECTOR = "input[name='password']"
    SUBMIT_SELECTOR = "input[type='submit']"

    browser.get(base_url + "/admin/login/")

    username_input = browser.find_element_by_css_selector(USERNAME_SELECTOR)
    password_input = browser.find_element_by_css_selector(PASSWORD_SELECTOR)
    submit_button = browser.find_element_by_css_selector(SUBMIT_SELECTOR)

    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()
