from selenium.webdriver.common.by import By
import time

def highlight_by_element(driver, xpath, color="red", thickness=3):
    """
    Highlights a web element by XPath using JavaScript.

    :param driver: Selenium WebDriver instance
    :param xpath: XPath string
    :param color: Border color
    :param thickness: Border thickness in px
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

        return element, original_style  # Return for reverting if needed

    except Exception as e:
        print(f"❌ Failed to highlight element: {e}")
        return None, None



def sleep_for(seconds: int | float, reason: str = ""):
    if reason:
        print(f"⏳ Sleeping for {seconds} seconds: {reason}")
    time.sleep(seconds)
