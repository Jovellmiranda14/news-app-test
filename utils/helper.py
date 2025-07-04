import os
import time
from typing import List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


def sleep_for(seconds: int | float, reason: str = ""):
    """
    Sleeps for a specified number of seconds with an optional reason for logging.
    """
    if reason:
        print(f"⏳ Sleeping for {seconds} seconds: {reason}")
    time.sleep(seconds)


def take_screenshot(
    driver: WebDriver, name_prefix="screenshot", save_dir="screenshots"
):
    """
    Takes a screenshot and saves it in the specified directory with a timestamped filename.

    :param driver: Selenium WebDriver instance
    :param name_prefix: Custom prefix for the screenshot file
    :param save_dir: Directory to save the screenshots
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name_prefix}_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)

    try:
        driver.save_screenshot(filepath)
        print(f"📸 Screenshot saved: {filepath}")
    except Exception as e:
        print(f"❌ Failed to save screenshot: {e}")


def highlight_multiple_elements(
    driver: WebDriver,
    xpaths: List[str],
    thickness: int = 3,
):
    """
    Highlights multiple elements using a fixed color ("red") and a predefined screenshot name.
    Screenshot will always be saved as 'highlighted_elements.png' (with timestamp if implemented).
    """
    highlight_color = "pink"
    screenshot_name = "highlighted_elements"

    try:
        for xpath in xpaths:
            element = driver.find_element(By.XPATH, xpath)
            highlight_style = f"border: {thickness}px solid {highlight_color};"
            driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element,
                highlight_style,
            )

        take_screenshot(driver, name_prefix=screenshot_name)

    except Exception as e:
        print(f"❌ Failed to highlight multiple elements: {e}")
        take_screenshot(driver, name_prefix="highlight_multiple_error")


def highlight_by_element(
    driver: WebDriver,
    xpath: str,
    color="red",
    thickness=3,
    screenshot_name="highlighted_elements",
):
    """
    Highlights a web element by XPath using JavaScript.
    Takes a screenshot even on success.
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        original_style = element.get_attribute("style")

        highlight_style = f"border: {thickness}px solid {color};"
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            highlight_style,
        )

        # Screenshot on success
        take_screenshot(driver, name_prefix=screenshot_name)
        return element, original_style

    except Exception as e:
        print(f"❌ Failed to highlight element: {e}")
        take_screenshot(driver, name_prefix="highlight_error")
        return None, None


def type_and_submit(
    driver: WebDriver,
    xpath: str,
    value: str,
    press_enter: bool = True,
):
    """
    Types a value into an input field located by XPath and optionally presses Enter.

    :param driver: Selenium WebDriver instance
    :param xpath: XPath of the input field
    :param value: Text to type into the field
    :param press_enter: If True, submits the input by pressing Enter
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        element.clear()
        element.send_keys(value)

        if press_enter:
            element.send_keys(Keys.RETURN)

    except Exception as e:
        print(f"❌ Failed to type and submit input: {e}")
