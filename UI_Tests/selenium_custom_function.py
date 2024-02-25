import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By



def init_driver(url):
    """
    init_driver function is used to initialize the driver

    :param url: the url to open in the browser
    :return: new webdriver obj
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def handle_element(driver, selector, value=''):
    """
    handle_element finds the element by its CSS selectors then handle
    the situation if to send keys or to click buttons

    :param driver: driver obj from the code to handle the elements
    :param selector: dictionary which contains the css selector of an element
    :param value:  none obj but if its given we will send keys otherwise click the element
    :return: None
    """

    time.sleep(1)
    element = driver.find_element(By.CSS_SELECTOR, selector)
    if value:
        element.send_keys(value)
    else:
        element.click()


def get_element_as_number(driver, selector):
    """
    gets the value of an element as a float number
    :param driver: driver to retrieve the elements
    :param selector: the str css selector
    :return:  the element content in float
    """
    element = driver.find_element(By.CSS_SELECTOR, selector)
    return float(element.text)


def parse_date(date_string):
    date_format = "%b %d, %Y %I:%M:%S %p"
    fixed_date = datetime.strptime(date_string, date_format)
    return str(fixed_date)



