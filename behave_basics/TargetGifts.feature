Feature: Target Gifts

  Background:
    Given Navigate to https://www.target.com/

  Scenario: Navigate to the page

  Scenario: Search for gifts
    When Search for Gift Ideas

  Scenario Outline: Verify searched page's headers
    When Search for <search_item>
    Then Verify header of the page contains <search_item>

    Examples:
      | search_item |
      | Gift Ideas  |
      | iphone      |

  Scenario: Gift idea - Tech with price under $25
    Given Navigate to https://www.target.com/c/gift-ideas/-/N-96d2i?lnk=snav_rd_gifts&redirect=true
    When Gift idea: select Tech from Gifts for whatever
    When Gift idea: select Under $25 from Gifts by price
    Then Verify all prices < 25

  Scenario: Gifts - Price validation
    When Search for Gift Ideas
    When Gift idea: select Her from Who are you shopping for?
    When Gift idea: select Gifts under $15 from Great gifts for any budget
    Then Collect all items on the first page into collected_items
    Then Verify all prices < 15
      | context.collected_items |

