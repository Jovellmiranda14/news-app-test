import os
import time
from typing import List
from datetime import datetime
from threading import Timer
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    Automatically deletes the screenshot after 30 seconds.

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

        # Schedule deletion after 30 seconds
        Timer(20, delete_file, args=(filepath,)).start()

    except Exception as e:
        print(f"❌ Failed to save screenshot: {e}")


def delete_file(filepath):
    """Deletes the file if it exists."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️ Screenshot deleted: {filepath}")
    except Exception as e:
        print(f"❌ Failed to delete screenshot: {e}")


def highlight_multiple_elements(
    driver: WebDriver,
    xpaths: List[str],
    thickness: int = 3,
):
    """
    Scrolls each element into view and highlights it using a fixed color ("pink").
    Then takes a screenshot of the highlighted elements.
    """
    highlight_color = "pink"
    screenshot_name = "highlighted_elements"

    try:
        for xpath in xpaths:
            # Scroll into view using the helper
            element = scroll_into_view(driver, xpath)
            if not element:
                print(f"⚠️ Skipping highlight for missing element: {xpath}")
                continue

            highlight_style = f"border: {thickness}px solid {highlight_color};"
            driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element,
                highlight_style,
            )

        # Screenshot after all highlights
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
    Scrolls the element into view using the scroll_into_view() helper.
    Takes a screenshot even on success.
    """
    try:
        # Scroll and get the element
        element = scroll_into_view(driver, xpath)
        if not element:
            raise Exception("Element could not be scrolled into view.")

        original_style = element.get_attribute("style")
        highlight_style = f"border: {thickness}px solid {color};"

        # Apply highlight via JavaScript
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            highlight_style,
        )

        take_screenshot(driver, name_prefix=screenshot_name)
        return element, original_style

    except Exception as e:
        print(f"❌ Failed to highlight element: {e}")
        take_screenshot(driver, name_prefix="highlight_error")
        return None, None


def type_only(
    driver: WebDriver,
    xpath: str,
    value: str,
):
    """
    Types a value into an input field after ensuring it is visible and interactable.
    Does NOT press Enter.

    :param driver: Selenium WebDriver instance
    :param xpath: XPath of the input field
    :param value: Text to type into the field
    """
    try:
        element = scroll_into_view(driver, xpath)
        if not element:
            raise Exception("Element not found to type into.")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.clear()
        element.send_keys(value)
        print(f"⌨️ Typed '{value}' into {xpath}")

    except Exception as e:
        print(f"❌ Failed to type into input: {e}")
        take_screenshot(driver, name_prefix="type_error")


def wait_for_element(driver: WebDriver, xpath: str, timeout: int = 10):
    """
    Waits for an element to be present in the DOM and returns it.

    :param driver: Selenium WebDriver instance
    :param xpath: XPath of the element to wait for
    :param timeout: Maximum wait time in seconds
    :return: WebElement if found, else None
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"❌ Timeout waiting for element: {xpath} — {e}")
        return None


def scroll_into_view(driver: WebDriver, xpath: str, timeout: int = 10):
    """
    Waits for the element to appear, then scrolls it into view using JavaScript.

    :param driver: Selenium WebDriver instance
    :param xpath: XPath of the element to scroll into view
    :param timeout: Max wait time in seconds
    :return: The WebElement if found, else None
    """
    try:
        # Wait for element to be present in the DOM
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Scroll into view
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )
        return element

    except Exception as e:
        print(f"❌ Failed to scroll to element: {xpath} — {e}")
        return None
