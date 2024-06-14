import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR')


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def get_element(self, locator):
        try:
            element = self.browser.driver.find_element(By.XPATH, locator)
            return element
        except NoSuchElementException:
            self.capture_screenshot()
            raise

    def get_elements(self, locator):
        try:
            elements = self.browser.driver.find_elements(By.XPATH, locator)
            return elements
        except NoSuchElementException:
            self.capture_screenshot()
            raise

    def capture_screenshot(self):
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{now}.png")
        self.browser.driver.save_screenshot(screenshot_path)
        print(f"Screenshot captured and saved to {screenshot_path}")
