Feature: The recommendation store service back-end
    As a E-commerce catalog service user
    I need a RESTful recommendation service
    So that I can recommend customer based on the current product

Background:
    Given the following recs
        | product_id | product_name | rec_id | rec_name | rec_type  | like_num |
        | 1          | foo          | 2      | bar      | UP_SELL   | 0        |
        | 2          | baz          | 3      | qux      | CROSS_SELL| 0        |
        | 3          | quux         | 4      | quuz     | ACCESSORY | 0        |
        | 4          | corge        | 5      | grault   | BUY_WITH  | 0        |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "Rec ID" to "0"
    And I set the "Product ID" to "1"
    And I set the "Product Name" to "foo"
    And I set the "Rec ID" to "2"
    And I set the "Rec Name" to "bar"
    And I select "Cross Sell" in the "Rec Type" dropdown
    And I set the "Like Num" to "0"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Rec ID" field should be empty
    And the "Product ID" field should be empty
    And the "Product Name" field should be empty
    And the "Rec ID" field should be empty
    And the "Rec Name" field should be empty
    And the "Rec Type" field should be empty
    And the "Like Num" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "1" in the "Product ID" field
    And I should see "foo" in the "Product Name" field
    And I should see "2" in the "Rec ID" field
    And I should see "bar" in the "Rec Name" field
    And I should see "Cross Sell" in the "Rec Type" dropdown
    And I should see "0" in the "Like Num" field

Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "foo" in the results
    And I should see "baz" in the results
    And I should see "quux" in the results
    And I should see "corge" in the results
    And I should not see "bik" in the results

# Scenario: Search for dogs
#     When I visit the "Home Page"
#     And I set the "Category" to "dog"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should not see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Search for available
#     When I visit the "Home Page"
#     And I select "True" in the "Available" dropdown
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should see "sammy" in the results
#     And I should not see "leo" in the results

# Scenario: Update a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I change "Name" to "Boxer"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see the message "Success"
#     And I should see "Boxer" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see the message "Success"
#     And I should see "Boxer" in the results
#     And I should not see "fido" in the results
