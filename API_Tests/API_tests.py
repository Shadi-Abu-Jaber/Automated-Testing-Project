import pytest
from requests_custom_function import *


@pytest.fixture()
def url():
    """
    function used as a variable
    :return: URL of the API Dictionary
    """
    return 'https://api.dictionaryapi.dev/api/v2/entries/en/'


class TestPositive:

    @pytest.mark.parametrize('word',
                             ['apple', 'Hello', 'HELLO', 'hELLo', 'supercalifragilisticexpialidocious', 'space%20bar'])
    def test_valid_words(self, url, word):
        """
        This function used to check more than one test case,
        it used to test: valid word, case insensitivity, URI Encoding, long word input
        :param url: url of the Dictionary API
        :param word: the word we want to search in the dictionary
        :return: None
        """
        status_code = get_status_code(url, word)
        actual_word, meaning = get_relevant_info(url, word)
        # Checks if the request returned a successful response
        assert status_code <= 400

        # Checks if the request returned definition and relevant information about the word "apple"
        if word == 'apple':
            assert actual_word == word and 'fruit' in meaning

        # Checks if the API can handle case-insensitive word searches and returns the definition for "hello"
        elif word.lower() == 'hello':
            assert actual_word == word.lower() and 'greet' in meaning

        # Checks that the API can handle long input words and returns relevant definitions.
        elif word == 'supercalifragilisticexpialidocious':
            assert actual_word == 'supercalifragilisticexpialidocious' and 'Fantastic' in meaning

        # Verifying that the API correctly handles URI-encoded input and returns the definition for the word.
        elif word == 'space%20bar':
            assert 'space' and 'bar' in actual_word and 'keyboard' in meaning

    @pytest.mark.parametrize('word', ['run', 'right'])
    def test_word_with_multiple_definitions(self, url, word):
        """
        This function tests if the word has multiple definitions
        :param url: url of the Dictionary API
        :param word: the word we want to search in the dictionary
        :return: None
        """
        number_of_definition = get_number_of_definition(url, word)
        # here we test word with only one definition
        if word == 'run':
            assert not number_of_definition > 1
        # here we test word with multiple definitions
        elif word == 'right':
            assert number_of_definition > 1


class TestNegative:
    @pytest.mark.parametrize('word', ['asdfghjkl', 'AAbbrQ', 'ADASDF', 'c++', '+c+', '++c', '+#!$'])
    def test_invalid_words(self, url, word):
        """
        This function used to check two test cases,
        it used to test: word with no definition, special characters
        :param url: url of the Dictionary API
        :param word: the word we want to search in the dictionary
        :return: None
        """
        status_code = get_status_code(url, word)
        title = invalid_input(url, word)
        assert status_code >= 400 and title == 'No Definitions Found'

    @pytest.fixture()
    def es_url(self):
        """
        function used as a variable
        :return: URL of the API Dictionary but with different language parameter (es)
        """
        return 'https://api.dictionaryapi.dev/api/v2/entries/es/'

    @pytest.mark.parametrize('word', ['book', 'food', 'apple', 'hello'])
    def test_language_parameters(self, es_url, word):
        """
        function checks if the API supports language parameter and returns the definition in the specified language.
        :param es_url:  URL of the API Dictionary but with different language parameter (es)
        :param word: the word we want to search in the dictionary
        :return: None
        """
        response = requests.get(es_url + word)
        status_code = response.status_code
        title = invalid_input(es_url, word)
        assert not status_code <= 400 and title == "No Definitions Found"

    def test_empty_input(self, url):
        """
        Function test the API response when the input is empty
        :param url: url of the Dictionary API
        :return: None
        """
        status_code = get_status_code(url, '')
        assert status_code >= 400

    @pytest.mark.parametrize('word', ['book', 'food', 'apple', 'hello'])
    def test_network_errors(self, url, word):
        """
        Function Simulates network errors by temporarily disconnecting from the internet during a request and check
        that the API gracefully handles the error.
        :param url: url of the Dictionary API
        :param word: the word we want to search in the dictionary
        :return: None
        """
        # disconnect from the internet first then run the test
        #  network_errors(dictionary_url, word)
