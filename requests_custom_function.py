import requests


def get_status_code(url, word):
    """
    Function sends a request then returns the status code of the response
    :param url: Dictionary API URL
    :param word: any word to search in the dictionary
    :return: status code
    """
    # Sending the request
    response = requests.get(url + word)
    # Store status code in a variable
    status_code = response.status_code
    return status_code


def get_response_as_json(url, word):
    """
    Function sends a request then returns JSON
    :param url: Dictionary API URL
    :param word: any word to search in the dictionary
    :return: response as JSON
    """
    try:
        # Sending the request
        response = requests.get(url + word)
        # Store JSON in a variable
        data_as_json = response.json()
        if response.status_code >= 400:
            raise Exception('invalid status code')
        return data_as_json
    except Exception:
        return None


def invalid_input(url, word):
    """
    Function used to test invalid word and check if the right message appears
    :param url: Dictionary API URL
    :param word: any word to search in the dictionary
    :return: 'no definition found' message
    """
    response = requests.get(url + word)
    message = response.json()['title']
    return message


def network_errors(url, word):
    """
    Function used to test the situation when a network error occurs
    :param url: Dictionary API URL
    :param word: any word to search in the dictionary
    :return: None
    """
    try:
        response = requests.get(url + word)
        # If a network error doesn't occur, the test should fail
        assert False, "Network error not simulated"
    except requests.exceptions.ConnectionError:
        # Simulated network error, the test should pass
        pass


def get_relevant_info(url, word):
    """
    Function used to get relevant information about the searched word
    :param url: Dictionary API URL
    :param word: any word to search in the dictionary
    :return: None
    """
    try:
        response = requests.get(url + word)
        # Retrieving the word
        searched_word = response.json()[0]['word']
        # Retrieving the word definition
        word_definition = response.json()[0]['meanings'][0]['definitions'][0]['definition']
        if response.status_code >= 400:
            raise Exception('invalid status code')
        return searched_word, word_definition
    except None:
        return None


def get_number_of_definition(url, word):
    """
    Function used to get number of definitions of the searched word
    :param url: Dictionary API URL
    :param word: any word to search in the dictionary
    :return: None
    """
    try:
        response = requests.get(url + word)
        number_of_definition = len(response.json()[0]['meanings'][0]['definitions'])
        if response.status_code >= 400:
            raise Exception('invalid status code')
        return number_of_definition
    except None:
        return None
