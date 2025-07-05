from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from locators.home_page_selectors import HomePageSelectors
from utils.helper import (
    sleep_for,
    highlight_by_element,
    type_only,
    highlight_multiple_elements,
)


class HomePage:
    def __init__(self, driver):
        # Store the Selenium WebDriver instance
        self.driver = driver

    def run(self, url, query):
        try:
            # Step 1: Load the website
            self.driver.get(url)
            sleep_for(2, "loading page")

            # Step 2: Highlight and type search query
            highlight_by_element(self.driver, HomePageSelectors.SEARCH_INPUT)
            sleep_for(2, "highlighted search input before typing")
            type_only(
                driver=self.driver,
                xpath=HomePageSelectors.SEARCH_INPUT,
                value=query,
            )
            sleep_for(2, "typed search query without submitting")

            # Step 3: Highlight and click search button (if available)
            if hasattr(HomePageSelectors, "SEARCH_BUTTON"):
                highlight_by_element(
                    self.driver, HomePageSelectors.SEARCH_BUTTON)
                try:
                    search_button = self.driver.find_element(
                        By.XPATH, HomePageSelectors.SEARCH_BUTTON
                    )
                    sleep_for(3, "waiting before clicking search button")
                    search_button.click()
                except Exception as e:
                    print(f"❌ Failed to click search button: {e}")

            sleep_for(3, "waiting for search results")

            # Step 4: Retrieve top 3 article titles
            xpaths = [
                HomePageSelectors.FIRST_ARTICLE,
                HomePageSelectors.SECOND_ARTICLE,
                HomePageSelectors.THIRD_ARTICLE,
            ]
            highlight_multiple_elements(self.driver, xpaths)
            articles = [
                self.driver.find_element(By.XPATH, xpath).text for xpath in xpaths
            ]

            # Step 5: Retrieve image source
            image_src = None
            try:
                image = self.driver.find_element(
                    By.XPATH, HomePageSelectors.IMAGE_1)
                sleep_for(1, "highlighted image before getting src")
                image_src = image.get_attribute("src")
            except Exception as e:
                print(f"❌ Error retrieving image: {e}")

            # Final: Return all gathered data
            return {"articles": articles, "image": image_src}

        except Exception as e:
            print(f"❌ Unexpected error in run(): {e}")
            return {"articles": [], "image": None}
