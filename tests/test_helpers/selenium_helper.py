from selenium.webdriver.support.select import Select

def get_selected_option(browser, css_selector):
    # Takes a css selector for a <select> element and returns the value of
    # the selected option
    select = Select(browser.find_element_by_css_selector(css_selector))
    return select.first_selected_option.get_attribute('value')
