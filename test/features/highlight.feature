Feature: Search News
  As a user
  I want to search for technology news
  So that I can read relevant articles

  Scenario: Highlight and search technology news
    Given I launch the browser and go to the homepage
    When I scroll to and highlight the search bar
    And I type "technology" in the search bar and press Enter
    Then articles should be highlighted

