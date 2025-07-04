from utils.driver_setup import create_driver
from pages.home_page import HomePage
from dotenv import load_dotenv
import os
from data.home_page_data import HomePageData
# Load .env variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

driver = create_driver(headless=False)

try:
    homepage = HomePage(driver)
    homepage.load(BASE_URL)
    print(f"✅ Site loaded: {BASE_URL}")

    homepage.search_news(HomePageData.SEARCH_INPUT_DATA)
    print(f"🔍 Search completed for '{HomePageData.SEARCH_INPUT_DATA}'")

    # articles = homepage.get_top_articles()
    # print("\n📰 Top Articles:")
    # for i, title in enumerate(articles, 1):
    #     print(f"{i}. {title}")

finally:
    driver.quit()
    print("\n🚪 Browser closed.")
