from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from locators.home_page_selectors import HomePageSelectors
from utils.helper import (
    sleep_for,
    highlight_by_element,
    type_and_submit,
    highlight_multiple_elements,
)


class HomePage:
    def __init__(self, driver):
        # Store the Selenium WebDriver instance
        self.driver = driver

    def load(self, url):
        # Navigate to the given URL
        self.driver.get(url)
        sleep_for(2, "loading page")

    def search_news(self, query):
        # Type the query but do NOT press Enter
        type_and_submit(
            driver=self.driver,
            xpath=HomePageSelectors.SEARCH_INPUT,
            value=query,
            press_enter=False,
        )

        # Optional: Highlight the search button for visibility
        if hasattr(HomePageSelectors, "SEARCH_BUTTON"):
            highlight_by_element(self.driver, HomePageSelectors.SEARCH_BUTTON)

            # Press the search button (click)
            try:
                search_button = self.driver.find_element(
                    By.XPATH, HomePageSelectors.SEARCH_BUTTON
                )
                search_button.click()
            except Exception as e:
                print(f"❌ Failed to click search button: {e}")

        # Wait for search results to load
        sleep_for(3, "waiting for search results")

    def get_top_3_articles(self):
        try:
            xpaths = [
                HomePageSelectors.FIRST_ARTICLE,
                HomePageSelectors.SECOND_ARTICLE,
                HomePageSelectors.THIRD_ARTICLE,
            ]

            # 🔍 Highlight all top 3 articles
            highlight_multiple_elements(self.driver, xpaths)

            # 📰 Retrieve and return their text
            return [self.driver.find_element(By.XPATH, xpath).text for xpath in xpaths]

        except Exception as e:
            print(f"❌ Error getting top 3 articles: {e}")
            return []

    def get_the_image(self):
        try:
            # Locate the image
            image = self.driver.find_element(By.XPATH, HomePageSelectors.IMAGE_1)

            # Optional wait for visibility or screenshot
            sleep_for(1, "highlighted image before getting src")

            # Return the image source URL
            return image.get_attribute("src")

        except Exception as e:
            # Log error if image retrieval fails
            print(f"Error retrieving image: {e}")
            return None
