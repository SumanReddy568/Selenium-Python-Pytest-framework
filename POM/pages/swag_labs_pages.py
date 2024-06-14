from POM.pages.base_page import BasePage
from POM.locators.swag_labs_locators import SwagLabs as el


class LoginPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def login(self, username, password):
        self.get_element(el.USER_NAME_PLACEHOLDER).send_keys(username)
        self.get_element(el.PASSWORD_PLACEHOLDER).send_keys(password)
        self.get_element(el.LOGIN_BUTTON).click()

    def place_an_order_in_swag_labs(self, first_name, last_name, zip_code):
        self.get_element(el.SWAG_LABS_BAG_HEADER).click()
        self.get_element(el.ADD_TO_CART_BUTTON).click()
        self.get_element(el.SHOPPING_CART_BUTTON).click()
        self.get_element(el.CHECKOUT_BUTTON).click()
        self.get_element(el.CHECKOUT_FIRST_NAME).send_keys(first_name)
        self.get_element(el.CHECKOUT_LAST_NAME).send_keys(last_name)
        self.get_element(el.CHECKOUT_ZIP_CODE).send_keys(zip_code)
        self.get_element(el.CHECKOUT_CONTINUE_BUTTON).click()
        self.get_element(el.FINISH_BUTTON).click()
        notification = self.get_element(el.DISH_PATCHED_TEXT).text
        return notification
