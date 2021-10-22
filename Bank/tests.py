from src.domain.entity import get_length, get_day, get_amount, get_tip
from src.functions.functions import option_e, option_d_max, option_d_sum
from src.ui.console import set_up


def test_add_transaction(t_list):
    """
    tests if the transactions are correct
    """
    for i in range(get_length(t_list)):
        day = get_day(t_list[i])
        amount = get_amount(t_list[i])
        tip = get_tip(t_list[i])
        if not 0 < day < 30:
            raise ValueError("Unexpected day of month \n")
        if amount <= 0:
            raise ValueError("Amount cannot be negative or equal to 0 \n")
        if not (tip == 'in' or tip == 'out'):
            raise ValueError("Transaction types can only be 'in' or 'out' \n")


def test_get_length(t_list):
    """
    tests if the length is correct
    """
    if not get_length(t_list) == 10:
        raise ValueError("Wrong number of transactions")


def test_option_d_max(t_list, option):
    tip, day, sum = option_d_max(t_list, option)
    if tip != 'out':
        raise ValueError("Max option is not working properly")
    if day != 26:
        raise ValueError("Max option is not working properly")
    if sum != 253:
        raise ValueError("Max option is not working properly")


def test_option_d_sum1(t_list, option):
    tip, sum = option_d_sum(t_list, option)
    if tip != 'in ':
        raise ValueError("Sum option is not working properly")
    if sum != 4500:
        raise ValueError("Sum option is not working properly")


def test_option_d_sum2(t_list, option):
    tip, sum = option_d_sum(t_list, option)
    if tip != 'out ':
        raise ValueError("Sum option is not working properly")
    if sum != -903:
        raise ValueError("Sum option is not working properly")


def test_option_e1(t_list, option):
    t_list = option_e(t_list, option)
    if get_length(t_list) != 1:
        raise ValueError("Filter option is not working properly")


def test_option_e2(t_list, option):
    t_list = option_e(t_list, option)
    if get_length(t_list) != 0:
        raise ValueError("Filter option is not working properly")


def test_all():
    """
    computes all the available tests
    """
    t_list = set_up()

    test_option_d_sum1(t_list, 'in ')
    test_option_d_sum2(t_list, 'out ')
    test_option_d_max(t_list, 'out 26 ')
    test_add_transaction(t_list)
    test_get_length(t_list)
    test_option_e1(t_list, 'in 1001 ')
    test_option_e2(t_list, 'out ')

