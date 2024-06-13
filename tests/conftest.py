import os
import sys
import pytest
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from datetime import datetime
from dotenv import load_dotenv

# Add the parent directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

LOG_DIR = os.getenv('LOG_DIR')
REPORTS_DIR = os.getenv('REPORTS_DIR')
SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR')
DRIVER_EXECUTABLE_PATH = os.getenv('DRIVER_EXECUTABLE_PATH')
CONFIG_INI = os.getenv('CONFIG_INI')

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
def chrome_driver(request, url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        print("Initialized Chrome WebDriver using WebDriver Manager.")
    except Exception as e:
        print(f"Failed to initialize Chrome WebDriver using WebDriver Manager: {e}")
        if os.path.exists(DRIVER_EXECUTABLE_PATH):
            driver = webdriver.Chrome(service=ChromeService(DRIVER_EXECUTABLE_PATH))
            print("Initialized Chrome WebDriver using executable path.")
        else:
            raise RuntimeError("ChromeDriver executable not found.")
    driver.maximize_window()

    # Navigate to the URL retrieved from the 'url' fixture
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

    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def url():
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read(CONFIG_INI)

    # Get URL from config.ini
    url = config.get('URLs', 'login_page')

    return url
