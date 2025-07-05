from selenium import webdriver  # Main Selenium module for browser automation
from webdriver_manager.chrome import (
    ChromeDriverManager,
)  # Automatically manages ChromeDriver installation
from selenium.webdriver.chrome.service import (
    Service,
)  # Controls the ChromeDriver background service
from selenium.webdriver.chrome.options import (
    Options,
)  # Used to configure browser startup options


def create_fast_driver(headless=False):
    # Create Chrome options to customize browser behavior
    options = Options()

    if headless:
        # Use new headless mode (more stable in modern Chrome versions)
        options.add_argument("--headless=new")

    # Disable GPU acceleration (not needed in headless mode)
    options.add_argument("--disable-gpu")

    # Disable the Chrome sandbox (required in some environments like Docker or CI/CD)
    options.add_argument("--no-sandbox")

    # Avoid using /dev/shm for shared memory (prevents crashes in limited environments)
    options.add_argument("--disable-dev-shm-usage")

    # Suppress most ChromeDriver logs (log level 3 = ERROR only)
    options.add_argument("--log-level=3")

    # Remove "Chrome is being controlled by automated test software" warning and suppress logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Disable images and fonts to speed up page loading and reduce resource usage
    options.add_experimental_option(
        "prefs",
        {"profile.managed_default_content_settings.fonts": 2},  # 2 = block fonts
    )

    # Set up ChromeDriver service using the correct driver version for your system
    service = Service(ChromeDriverManager().install())

    # Launch and return the configured Chrome WebDriver
    return webdriver.Chrome(service=service, options=options)
