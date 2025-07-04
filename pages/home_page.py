# Required imports from Selenium and project-specific modules
from selenium.webdriver.common.by import By  # For locating elements (e.g., By.XPATH)
from selenium.webdriver.common.keys import Keys  # For keyboard keys (e.g., ENTER)
from locators.home_page_selectors import HomePageSelectors  # XPath locators for homepage
from utils.helper import sleep_for  # Custom sleep with log messages
from utils.helper import highlight_by_element  # Highlights elements using JS for debugging


# Page Object Model class for interactions on the homepage
class HomePage:
    def __init__(self, driver):
        # Store the Selenium WebDriver instance for use in methods
        self.driver = driver

    def load(self, url):
        # Navigates the browser to the specified URL
        self.driver.get(url)

        # Waits 2 seconds with a custom log message
        sleep_for(2, "loading page")

    def search_news(self, query):
        # Locates the search input field using its XPath
        search_input = self.driver.find_element(
            By.XPATH, HomePageSelectors.SEARCH_INPUT
        )

        # Highlights the input field visually for debugging (adds red border)
        highlight_by_element(self.driver, HomePageSelectors.SEARCH_INPUT)

        # Types the given query into the search box
        search_input.send_keys(query)

        # Presses Enter to submit the search
        search_input.send_keys(Keys.RETURN)

        # Waits 3 seconds for search results to appear
        sleep_for(3, "waiting for search results")

    def get_top_articles(self, count=5):
        # Finds all article title elements on the page using the defined XPath
        articles = self.driver.find_elements(By.XPATH, HomePageSelectors.ARTICLE_TITLES)

        # Extracts the text of each article and returns the top `count` items (default: 5)
        return [article.text for article in articles[:count]]

    def get_the_image(self):
        try:
            # Attempts to locate the specific image using XPath
            image = self.driver.find_element(By.XPATH, HomePageSelectors.IMAGE_1)

            # Optional pause for debugging or visual confirmation
            sleep_for(1, "highlighted image before getting src")

            # Returns the image's source URL
            return image.get_attribute("src")

        except Exception as e:
            # Handles any errors (e.g., image not found) and prints a readable message
            print(f"Error retrieving image: {e}")
            return None
