Feature: Target Gifts

  Scenario: Navigate to the page
    Given Navigate to https://www.target.com/

  Scenario: Search for gifts
    Given Navigate to https://www.target.com/
    When Search for Gift Ideas

   Scenario: Gift idea - Cell Phones
    Given Navigate to https://www.target.com/c/gift-ideas/-/N-96d2i?lnk=snav_rd_gifts&redirect=true
    When Gift idea: select Tech from Gifts for whatever
    When Gift idea: select Cell Phones from Explore gifts by category

  Scenario: Gift idea - Tech with price under $25
    Given Navigate to https://www.target.com/c/gift-ideas/-/N-96d2i?lnk=snav_rd_gifts&redirect=true
    When Gift idea: select Tech from Gifts for whatever
    When Gift idea: select Under $25 from Gifts by price

