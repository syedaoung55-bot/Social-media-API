from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest

# py -3 -m tests.test_calculations to execute this
# also using pytest pytest tests\test_calculations.py
# pytest -v for function and -s for print statements -x to stop on first failure of test

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account_balance():
    return BankAccount(9000)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5), (4, 8, 12), (77, 9, 86)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(8, 1) == 7

def test_multiply():
    assert multiply(7, 3) == 21

def test_divide():
    assert divide(4, 2) == 2


def test_bank_set_initial_value(bank_account_balance):
    assert bank_account_balance.balance == 9000

def test_bank_default_value(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_deposit_value(bank_account_balance):
    bank_account_balance.deposit(10000)
    assert bank_account_balance.balance == 19000

def test_bank_withdraw_value(bank_account_balance):
    bank_account_balance.withdraw(1600)
    assert bank_account_balance.balance == 7400

def test_bank_interest_value(bank_account_balance):
    bank_account_balance.collect_interest()
    assert bank_account_balance.balance == 9900


@pytest.mark.parametrize("deposited, withdrew, balance", [
    (1000, 800, 200), 
    (5678, 2168, 3510), 
    (2345, 1234, 1111), 
])
def test_transaction(zero_bank_account, deposited, withdrew, balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == balance

def test_insufficient_funds(bank_account_balance):
    with pytest.raises(InsufficientFunds):
        bank_account_balance.withdraw(10000)