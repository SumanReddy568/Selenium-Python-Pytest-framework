import os
import sys
import pytest
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR')
CONFIG_INI = os.getenv('CONFIG_INI')
LOG_DIR = os.getenv('LOG_DIR')
DRIVER_EXECUTABLE_PATH = os.getenv('DRIVER_EXECUTABLE_PATH')
REPORTS_DIR = os.getenv('REPORTS_DIR')
URL = os.getenv('login_page')
for directory in [LOG_DIR, REPORTS_DIR, SCREENSHOT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

# Configure logging
logging.basicConfig(filename=os.path.join(LOG_DIR, 'test_log.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Browser:
    def __init__(self, driver):
        self.driver = driver

    def go_to_url(self, url):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()

@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser_name")

@pytest.fixture(scope="session")
def url():
    
    # config = configparser.ConfigParser()
    # config.read(CONFIG_INI)
    return URL

@pytest.fixture(scope="session")
def browser(request, browser_name, url):
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        print("Initialized Chrome WebDriver using WebDriver Manager.")
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        driver.maximize_window()
        print("Initialized Firefox WebDriver using WebDriver Manager.")
    else:
        raise ValueError("Unsupported browser specified.")

    driver.get(url)

    def fin():
        if hasattr(request.node, 'wasxfail') and request.node.wasxfail:
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{now}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        else:
            print("No failure detected, skipping screenshot capture.")

    request.addfinalizer(fin)

    browser = Browser(driver)
    yield browser
    browser.quit()

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Name of the browser to run tests")
