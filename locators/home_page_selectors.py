class HomePageSelectors:
    SEARCH_INPUT = "//input[@type='text']"
    ARTICLE_TITLES = "//div[contains(@class, 'news-card')]//h2"
    IMAGE_1 = "(//img[@class='img-fluid position-absolute'])[3]"
    SEARCH_BUTTON = "//button[@type='submit']"
    FIRST_ARTICLE = "//div[normalize-space(text())='Plantaform Smart Indoor Garden Review: Rewarding but Risky']"
    SECOND_ARTICLE = "//div[normalize-space(text())='After Slashing Thousands of Jobs, Trump’s FDA Wants to Use AI to Rapidly Approve New Drugs']"
    THIRD_ARTICLE = "//div[normalize-space(text())='Physicists Solve a 50-Year Mystery About a Critically Important Molecule']"
