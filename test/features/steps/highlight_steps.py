import sys
import os

# Ensure root path is in sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from behave import given, when, then
from utils.helper import highlight_by_element, type_only, wait_for_element, sleep_for
from dotenv import load_dotenv
from utils.driver_setup import create_fast_driver
from locators.home_page_selectors import HomePageSelectors
from data.home_page_data import HomePageData

# ✅ Load environment variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    raise ValueError("❌ BASE_URL is not set in your .env file.")


@given("I launch the browser and go to the homepage")
def step_launch_browser(context):
    context.driver = create_fast_driver(headless=False)
    context.driver.get(BASE_URL)
    print(f"🌐 Navigated to {BASE_URL}")


@when("I scroll to and highlight the search bar")
def step_highlight_search_bar(context):
    element, _ = highlight_by_element(context.driver, HomePageSelectors.SEARCH_INPUT)
    sleep_for(1, "waiting after highlighting search bar")
    assert element is not None, "❌ Could not highlight search bar"
    print("🔍 Search bar highlighted.")


@when('I type "technology" in the search bar and press Enter')
def step_type_and_search(context):
    type_only(context.driver, HomePageSelectors.SEARCH_INPUT, HomePageData.TECHONOLOGY)
    sleep_for(1, "waiting after typing search query")
    print(f"🔤 Typed query: {HomePageData.TECHONOLOGY}")
    element, _ = highlight_by_element(context.driver, HomePageSelectors.SEARCH_BUTTON)
    assert element is not None, "❌ Could not find or highlight the search button."
    sleep_for(1, "waiting before clicking search button")
    element.click()
    print("✅ Typed query and clicked the search button.")


@then("articles should be highlighted")
def check_articles(context):
    xpaths = [
        HomePageSelectors.FIRST_ARTICLE,
        HomePageSelectors.SECOND_ARTICLE,
        HomePageSelectors.THIRD_ARTICLE,
    ]
    elements = []
    for xpath in xpaths:
        element, _ = highlight_by_element(context.driver, xpath)
        assert element is not None, f"❌ Could not highlight article at {xpath}"
        elements.append(element)

    print(f"📄 Highlighted {len(elements)} articles successfully.")


@then("I close the browser")
def step_close_browser(context):
    context.driver.quit()
