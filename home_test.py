from utils.driver_setup import create_fast_driver
from pages.home_page import HomePage
from dotenv import load_dotenv
import os
from data.home_page_data import HomePageData

# Load .env variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

driver = create_fast_driver(headless=False)

try:
    homepage = HomePage(driver)
    homepage.load(BASE_URL)
    print(f"✅ Site loaded: {BASE_URL}")

    query = HomePageData.TECHONOLOGY
    homepage.search_news(query)
    print(f"🔍 Search completed for '{query}'")

    top_articles = homepage.get_top_3_articles()
    if top_articles:
        print("📰 Top 3 articles:")
        for i, article in enumerate(top_articles, start=1):
            print(f"{i}. {article}")
    else:
        print("❌ No articles found or an error occurred while retrieving them.")

finally:
    driver.quit()
    print("\n🚪 Browser closed.")
