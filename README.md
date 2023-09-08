# Automation-Testing-Project

## Tested Demo Sites:
please take a quick look at the websites

 
UI Testing: https://www.globalsqa.com/angularJs-protractor/BankingProject/#/ 
(demo bank website)

API Testing: https://api.dictionaryapi.dev/api/v2/entries/en/<word>
(Dictionary website) 

## UI Test Cases:
- Log in to the system with one of the existing users and make a deposit of 250 and see that the account status has changed accordingly
- Log in to the system with administrator privileges, click on the Users button, delete one of the users you like
Write a test that checks that the action was actually performed
- Log in to the system as an administrator, add a new client, return to the administrator's screen and check that the client you entered is indeed
available
- Enter the bank as a user, make a deposit of NIS 1000 and withdraw NIS 250, check that the account balance is NIS 750
- Write a code that enters the system as an administrator and add a new account, check that you are at the appropriate url
- Log in to the system as a user and make a transfer of 1500. Make sure that the transfer has been made and appears in the transfer report.
- Enter the system as an administrator and check that you have exactly 5 customers in the system using the code
- Do a sanity check for the system
- Check that the system does not allow adding a new customer without a first name
- Enter the system as a user, check that the money deposit field does not accept textual values, only numbers

## API Test Cases:

- Valid Word Lookup:	

  Input: "apple"

  Expected Output: Successful response with the definition and relevant information about the word "apple".
 
- Word with Multiple Definitions:	

  Input: "run"

  Expected Output: Verify that the response contains multiple definitions for the word "run".
 
- Word with No Definitions:	

  Input: "asdfghjkl"

  Expected Output: Ensure that the response indicates that the word is not found or handle the case of no definitions.
 
- Case Insensitivity:

  Input: "Hello"

  Expected Output: Ensure that the API handles case-insensitive word searches and returns the definition for "hello".
 
- Special Characters:	

  Input: "c++"

  Expected Output: Validate that the API can handle special characters and return definitions for programming-related terms.
 
- URI Encoding:	

  Input: "space%20bar"

  Expected Output: Verify that the API correctly handles URI-encoded input and returns the definition for the corresponding word.
 
- Language Parameter:	

  Input: "book", language="es" (Spanish)

  Expected Output: Confirm that the API supports language parameter and returns the definition in the specified language.
 
- Empty Input:	

  Input: ""

  Expected Output: Check that the API handles empty input gracefully and returns an appropriate error response.
 
- Network Errors:	

  Simulate network errors by temporarily disconnecting from the internet during a request and ensure that the API gracefully handles 
  the error.
 
- Long Word Input:

  Input: "supercalifragilisticexpialidocious"

  Expected Output: Verify that the API can handle long input words and returns relevant definitions.





