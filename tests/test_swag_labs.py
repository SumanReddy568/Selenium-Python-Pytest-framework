import sys
import os
import logging
import configparser
from POM.pages.swag_labs_pages import LoginPage
from utils.helper.faker_helper import generate_fake_data
from POM.notifications.swag_labs_messages import SwagLabs

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = configparser.ConfigParser()
config_path = os.getenv('CONFIG_INI')

try:
    if config_path:
        config.read(config_path)
        username = config.get('Credentials', 'username')
        password = config.get('Credentials', 'password')
    else:
        raise FileNotFoundError("CONFIG_INI environment variable not set or file not found.")
except FileNotFoundError as e:
    logging.error(str(e))
    sys.exit(1)


def test_swag_labs_order_checkout(browser):
    try:
        first_name = generate_fake_data("first_name")
        last_name = generate_fake_data("last_name")
        zip_code = generate_fake_data("zip_code")
        logging.info("Test swag labs order checkout has started")
        login_page = LoginPage(browser)
        login_page.login(username, password)
        logging.info("Login successful")
        logging.info("Placing the order and checking out")
        notification = login_page.place_an_order_in_swag_labs(first_name, last_name, zip_code)
        assert notification == SwagLabs.DISPATCHED_MESSAGE
        logging.info(f"{notification}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
