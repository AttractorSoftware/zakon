Feature: PageIn
    A user should be go to page

Scenario: page_in
    Given I go to the main page
    And I press any link
    Then I should see page with title "Просмотр документа"