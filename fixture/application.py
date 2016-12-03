from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from fixture.navigation import NavigationHelper
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.soap import SOAPHelper


class Application:

    def __init__(self, browser, base_url, user, password):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.base_url = base_url
        self.user = user
        self.password = password
        self.navigation = NavigationHelper(self)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.soap = SOAPHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def ensure_confirm_page(self, text):
        try:
            WebDriverWait(self.wd, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".success-msg"), text))
        except TimeoutException:
            raise TimeoutException("\nConfirmation page was not loaded in due time.\n")

    def update_textbox(self, field, value):
        if value is not None:
            self.wd.find_element_by_id(field).click()
            self.wd.find_element_by_id(field).clear()
            self.wd.find_element_by_id(field).send_keys(value)

    def update_dropdown(self, field, value):
        if value is not None:
            item = Select(self.wd.find_element_by_id(field))
            item.select_by_visible_text(value)

    def update_checkbox(self, field, value):
        if not value:
            self.wd.find_element_by_id(field).click()

    def destroy(self):
        self.wd.quit()
