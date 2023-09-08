import pytest
from selenium_custom_function import *
from selenium.webdriver.common.alert import Alert


@pytest.fixture()
def log_in_url():
    """
    function used as a variable
    :return: url of the bank log in webpage
    """
    return 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login'


class TestDeposit:

    @pytest.fixture
    def css_selectors_1(self):
        """
        function used as a variable
        :return: dictionary contains css selectors(as str) of webpages elements
        """
        return {
            'customer log in button': 'body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button',
            'customers drop down': '#userSelect',
            'customer name': '#userSelect > option:nth-child(3)',
            'log in button': 'body > div > div > div.ng-scope > div > form > button',
            'first deposit button': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(2)',
            'amount input': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > div > input',
            'second deposit button': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button',
            'balance': 'body > div > div > div.ng-scope > div > div:nth-child(3) > strong:nth-child(2)',
            'transactions list': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)',
            'amount cell': '#anchor0 > td:nth-child(2)',
            'deposit successful message': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > span'
        }

    @pytest.mark.parametrize('amount_to_deposit', ['1', '250', '1500', '1000000'])
    def test_deposit_valid_amount(self, log_in_url, css_selectors_1, amount_to_deposit):
        """
        The function tests the deposit process when we insert a valid input
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_1: dictionary contains css selectors(as str) of webpages elements
        :param amount_to_deposit: the amount to be deposited
        :return: None
        """
        driver = init_driver(log_in_url)
        # performing the UI interactions by using selenium functions
        for key in css_selectors_1:

            if key == 'amount cell':
                break

            elif key == 'balance':
                # storing the balance value after the deposit process
                balance = get_element_as_number(driver, css_selectors_1[key])

            elif key == "amount input":
                # Inserting deposit amount
                handle_element(driver, css_selectors_1[key], amount_to_deposit)
            elif key == 'second deposit button':
                handle_element(driver, css_selectors_1[key])
                # storing the deposit date of the deposit process
                deposit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                handle_element(driver, css_selectors_1[key])

        driver.implicitly_wait(1)
        # locate the transactions table
        table_selector = "body > div > div > div.ng-scope > div > div:nth-child(2) > table"
        table = driver.find_element(By.CSS_SELECTOR, table_selector)
        # locate the rows of the transactions table
        rows_selector = "body > div > div > div.ng-scope > div > div:nth-child(2) > table > tbody > tr"
        rows = table.find_elements(By.CSS_SELECTOR, rows_selector)
        dates = []
        amounts = []
        # storing the cells values in a lists
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            date = cells[0].text
            dates.append(date)
            amount = cells[1].text
            amounts.append(amount)
        # the bank website shows the hours in dates without a zero when the hour's number is less than 10,
        # so I handle it to test dates, for example converting 2:15 to 02:15
        fixed_dates = []
        for date in dates:
            # Reformatting the dates then adding them to list
            fixed_dates.append(parse_date(date))

        assert float(amount_to_deposit) == float(amounts[-1]) and deposit_date == fixed_dates[-1]
        assert balance == float(amount_to_deposit)

    @pytest.mark.parametrize('amount_to_deposit', ['0', '-250', '-1000000', 'blablabla', 'BLABLABLA', 'BlAblAbLA'])
    def test_deposit_invalid_amount(self, log_in_url, css_selectors_1, amount_to_deposit):
        """
        The function tests the deposit process when we insert an invalid input
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_1: dictionary contains css selectors(as str) of webpages elements
        :param amount_to_deposit: the amount to be deposited
        :return: None
        """

        driver = init_driver(log_in_url)
        # performing the UI interactions by using selenium function
        for key in css_selectors_1:
            # we stop after clicking on deposit button to check if the successful message appeared
            if key == 'balance':
                break
            elif key == "amount input":
                handle_element(driver, css_selectors_1[key], amount_to_deposit)
            else:
                driver.implicitly_wait(1)
                handle_element(driver, css_selectors_1[key])

        driver.implicitly_wait(1)
        # locate the message that appears when the deposit process completed successfully
        message = driver.find_element(By.CSS_SELECTOR, css_selectors_1['deposit successful message'])
        # checking if the massage is displayed
        assert not message.is_displayed()


class TestBankManager:

    @pytest.fixture
    def css_selectors_2(self):
        """
        function used as a variable
        :return: dictionary contains css selectors(as str) of webpages elements
        """
        return {
            'bank manager log in button': 'body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(3) > button',
            'customers list': 'body > div > div > div.ng-scope > div > div.center > button:nth-child(3)',
            'delete Ron button': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > table > tbody > tr:nth-child(3) > td:nth-child(5) > button',
            'customers table': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > table',
            'customers table rows': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > table > tbody > tr'
        }

    @pytest.fixture()
    def deleted_account(self):
        """
        function used as a variable
        :return: account number of Ron Weasly
        """
        return '1007 1008 1009'

    def test_delete_customer(self, log_in_url, css_selectors_2, deleted_account):
        """
        The function tests the deletion process of one of the customer in customers list
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_2: dictionary contains css selectors(as str) of webpages elements
        :param deleted_account: the customer account to be deleted
        :return: None
        """
        driver = init_driver(log_in_url)
        # performing the UI interactions by using selenium function
        for key in css_selectors_2:
            driver.implicitly_wait(1)
            handle_element(driver, css_selectors_2[key])
        # locate the customers table
        table = driver.find_element(By.CSS_SELECTOR, css_selectors_2['customers table'])
        # locate the rows of the customers table
        rows = table.find_elements(By.CSS_SELECTOR, css_selectors_2['customers table rows'])

        acc_numbers = []
        # storing the cells values in a lists
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            account_number = cells[3].text
            acc_numbers.append(account_number)

        assert len(acc_numbers) == 4
        # checking that the customer is no longer exist in the customers list
        for acc in acc_numbers:
            assert deleted_account != acc

    @pytest.fixture
    def css_selectors_3(self):
        """
        function used as a variable
        :return: dictionary contains css selectors (as str) of webpage elements
        """
        return {
            'bank manager log in button': 'body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(3) > button',
            'first add customer button': 'body > div > div > div.ng-scope > div > div.center > button:nth-child(1)',
            'first name': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > div:nth-child(1) > input',
            'last name': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > div:nth-child(2) > input',
            'post code': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > div:nth-child(3) > input',
            'second add customer button': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > button',
            'customers': 'body > div > div > div.ng-scope > div > div.center > button:nth-child(3)',
            'customers table': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > table',
            'customers table rows': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > table > tbody > tr'
        }

    @pytest.fixture()
    def add_customer_url(self):
        """
        function used as a variable
        :return: url of the 'add new customer' webpage
        """
        return 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager/addCust'

    def test_url(self, log_in_url, css_selectors_3, add_customer_url):
        """
        The function tests if we are at the right url when we try to add a new customer
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_3: dictionary contains css selectors(as str) of webpages elements
        :param add_customer_url: url of the 'add new customer' webpage
        :return: None
        """
        driver = init_driver(log_in_url)
        for key in css_selectors_3:
            if key == 'last name':
                break
            else:
                handle_element(driver, css_selectors_3[key])
        assert driver.current_url == add_customer_url

    @pytest.mark.parametrize('first_name,last_name,post_code',
                             [('shadi', 'abu jaber', '1680500'), ('', 'abu jaber', '1680500'), ('shadi', '', '1680500'),
                              ('shadi', 'abu jaber', '')])
    def test_add_customer(self, log_in_url, css_selectors_3, add_customer_url, first_name, last_name, post_code):
        """
        The function tests adding new customer process in different cases and inputs(valid & invalid)
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_3: dictionary contains css selectors(as str) of webpages elements
        :param add_customer_url: url of the 'add new customer' webpage
        :param first_name: the given customer's first name
        :param last_name: the given customer's last name
        :param post_code: the given customer's post code
        :return: None
        """
        driver = init_driver(log_in_url)
        # performing the UI interactions by using selenium function
        for key in css_selectors_3:
            if key == 'first name':
                handle_element(driver, css_selectors_3[key], first_name)
            elif key == 'last name':
                handle_element(driver, css_selectors_3[key], last_name)
            elif key == 'post code':
                handle_element(driver, css_selectors_3[key], post_code)
            elif key == 'second add customer button':
                handle_element(driver, css_selectors_3[key])
                driver.implicitly_wait(1)
                # if the inputs are valid click on the accept button of the alert window
                if first_name != '' and last_name != '' and post_code != '':
                    Alert(driver).accept()
            else:
                driver.implicitly_wait(1)
                handle_element(driver, css_selectors_3[key])
        # locate the customers table
        table = driver.find_element(By.CSS_SELECTOR, css_selectors_3['customers table'])
        # locate the rows of the customers table
        rows = table.find_elements(By.CSS_SELECTOR, css_selectors_3['customers table rows'])

        first_names = []
        last_names = []
        post_codes = []
        # storing the cells values in an appropriate lists
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            first_name = cells[0].text
            first_names.append(first_name)
            last_name = cells[1].text
            last_names.append(last_name)
            post_code = cells[2].text
            post_codes.append(post_code)

        # here the function used to check invalid inputs
        if first_name == '' or last_name == '' or post_code == '':
            assert first_name not in first_names and last_name not in last_names and post_code not in post_codes

        # here the function used to check valid inputs
        else:
            assert first_name == first_names[-1] and last_name == last_names[-1] and post_code == post_codes[-1]


class TestSanity:
    @pytest.fixture()
    def css_selectors_5(self):
        """
        function used as a variable
        :return: dictionary contains css selectors(as str) of webpages elements
        """
        return {
            'customer log in button': 'body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button',
            'customers drop down': '#userSelect',
            'customer name': '#userSelect > option:nth-child(3)',
            'log in button': 'body > div > div > div.ng-scope > div > form > button',
            'first deposit button': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(2)',
            'deposit amount': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > div > input',
            'second deposit button': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button',
            'first withdrawal button': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(3)',
            'withdrawal amount': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > div > input',
            'second withdrawal button': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button',
            'transactions list': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)',
            'reset button': 'body > div > div > div.ng-scope > div > div.fixedTopBox > button:nth-child(3)',
            'log out button': 'body > div > div > div.box.mainhdr > button.btn.logout',
            'home button': 'body > div > div > div.box.mainhdr > button.btn.home',
            'bank manager button': 'body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(3) > button',
            'first add customer button': 'body > div > div > div.ng-scope > div > div.center > button:nth-child(1)',
            'first name': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > div:nth-child(1) > input',
            'last name': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > div:nth-child(2) > input',
            'post code': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > div:nth-child(3) > input',
            'second add customer button': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > button',
            'customers list': 'body > div > div > div.ng-scope > div > div.center > button:nth-child(3)',
            'open account button': 'body > div > div > div.ng-scope > div > div.center > button:nth-child(2)',
            'customer drop down': '#userSelect',
            'harry potter': '#userSelect > option:nth-child(3)',
            'currency drop down': '#currency',
            'rupee': '#currency > option:nth-child(4)',
            'process button': 'body > div > div > div.ng-scope > div > div.ng-scope > div > div > form > button'

        }

    @pytest.mark.parametrize('deposit_amount,withdrawal_amount,first_name,last_name,post_code',
                             [('250', '100', 'shadi', 'AJ', '1234')])
    def test_sanity(self, log_in_url, css_selectors_5, deposit_amount, withdrawal_amount, first_name, last_name,
                    post_code):
        """
        The function performs a sanity test to the whole bank website by doing a complete business process
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_5: dictionary contains css selectors(as str) of webpages elements
        :param deposit_amount: the amount to be deposited
        :param withdrawal_amount: the amount to be withdrawal
        :param first_name: the given customer's first name
        :param last_name: the given customer's last name
        :param post_code: the given customer's post code
        :return: None
        """
        driver = init_driver(log_in_url)
        # performing the UI interactions by using selenium function
        for key in css_selectors_5:
            # at every webpage we check the title
            assert 'XYZ Bank' in driver.title
            if key == "deposit amount":
                handle_element(driver, css_selectors_5[key], deposit_amount)
            elif key == 'withdrawal amount':
                handle_element(driver, css_selectors_5[key], withdrawal_amount)
            elif key == 'first name':
                handle_element(driver, css_selectors_5[key], first_name)
            elif key == 'last name':
                handle_element(driver, css_selectors_5[key], last_name)
            elif key == 'post code':
                handle_element(driver, css_selectors_5[key], post_code)
            elif key == 'second add customer button' or key == 'process button':
                handle_element(driver, css_selectors_5[key])
                # accepting the alert window
                Alert(driver).accept()
            else:
                handle_element(driver, css_selectors_5[key])


class TestBalance:
    @pytest.fixture
    def css_selectors_4(self):
        """
        function used as a variable
        :return: dictionary contains css selectors(as str) of webpages elements
        """
        return {
            'customer log in button': 'body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button',
            'customers drop down': '#userSelect',
            'customer name': '#userSelect > option:nth-child(3)',
            'log in button': 'body > div > div > div.ng-scope > div > form > button',
            'first deposit button': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(2)',
            'deposit amount': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > div > input',
            'second deposit button': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button',
            'first withdrawal button': 'body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(3)',
            'withdrawal amount': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > div > input',
            'second withdrawal button': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button',
            'balance': 'body > div > div > div.ng-scope > div > div:nth-child(3) > strong:nth-child(2)',
            'Transaction Failed message': 'body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > span'
        }

    @pytest.mark.parametrize('deposit_amount,withdrawal_amount', [('1000', '250'), ('250', '250'), ('250', '1000')])
    def test_balance(self, log_in_url, css_selectors_4, deposit_amount, withdrawal_amount):
        """
        The function tests the balance amount with different inputs,  to check if it is changes accordingly
        :param log_in_url: url of the bank log in webpage
        :param css_selectors_4: dictionary contains css selectors(as str) of webpages elements
        :param deposit_amount: the amount to be deposited
        :param withdrawal_amount: the amount to be withdrawal
        :return: None
        """
        driver = init_driver(log_in_url)
        # performing the UI interactions by using selenium function
        for key in css_selectors_4:
            if key == 'balance':
                balance = get_element_as_number(driver, css_selectors_4[key])
            elif key == 'deposit amount':
                handle_element(driver, css_selectors_4[key], deposit_amount)
            elif key == 'withdrawal amount':
                handle_element(driver, css_selectors_4[key], withdrawal_amount)
            else:
                handle_element(driver, css_selectors_4[key])

        # checking if the correct message  displayed when trying to withdrawal an amount that is greater than balance
        if balance < float(withdrawal_amount):
            message = driver.find_element(By.CSS_SELECTOR, css_selectors_4['Transaction Failed message'])
            assert message.is_displayed()
        # checking if the balance changes appropriately
        else:
            assert balance == float(deposit_amount) - float(withdrawal_amount)
