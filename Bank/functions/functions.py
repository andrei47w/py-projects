import datetime

from src.domain.entity import get_length, get_day, get_amount, get_tip, get_desc, set_amount, set_transaction


def add_transaction(t_list, day, amount, tip, desc):
    """
    adds a new transaction to the list
    :param: transaction's day, amount, type and desctription
    """
    if not 0 < day < 30:
        print("Unexpected day of month \n")
        return
    if amount <= 0:
        print("Amount cannot be negative or equal to 0 \n")
        return
    if not (tip == 'in' or tip == 'out'):
        print("Transaction types can only be 'in' or 'out' \n")
        return

    transaction = []
    transaction.append(day)
    transaction.append(amount)
    transaction.append(tip)
    transaction.append(desc)

    return set_transaction(t_list, transaction)


def option_a_add(t_list, option):
    """
    computes if the command requested is 'add'
    :param: the command as a string
    """
    now = datetime.datetime.now()
    amount = int(option[:option.find(' ')])
    option = option[option.find(' ') + 1:]
    tip = option[:option.find(' ')]
    option = option[option.find(' ') + 1:]
    desc = option[:-1]

    return add_transaction(t_list, now.day, amount, tip, desc)


def option_a_insert(t_list, option):
    """
    computes if the command requested is 'insert'
    :param: the command as a string
    """
    day = int(option[:option.find(' ')])
    option = option[option.find(' ') + 1:]
    amount = int(option[:option.find(' ')])
    option = option[option.find(' ') + 1:]
    tip = option[:option.find(' ')]
    option = option[option.find(' ') + 1:]
    desc = option

    return add_transaction(t_list, day, amount, tip, desc)


def condition_b(t_list, i, tip):
    """
    :return: True or False
    :param: the n th element of the list and the requested command
    """
    tip = tip[:-1]
    if tip.find(' ') == -1 and tip.isdigit() and get_day(t_list[i]) == int(tip): return True
    if tip.find(' ') == -1 and get_tip(t_list[i]) == tip: return True
    if tip.find(' ') != -1 and int(tip[:tip.find(' ')]) < get_day(t_list[i]) < int(tip[tip.find(' ') + 3:]): return True
    return False


def option_b_remove(t_list, tip):
    """
    computes if the command requested is 'remove'
    :param: the command as a string
    """
    pos = int(0)
    for i in range(get_length(t_list)):
        if condition_b(t_list, pos, tip):
            del t_list[pos]
            pos -= 1
        pos += 1

    return t_list


def option_b_replace(t_list, option):
    """
    computes if the command requested is 'replace'
    :param: the command as a string
    """
    day = int(option[:option.find(' ')])
    option = option[option.find(' ') + 1:]
    tip = option[:option.find(' ')]
    option = option[option.find(' ') + 1:]
    desc = option[:option.find(' ')]
    option = option[option.find(' ') + 1:]
    option = option[option.find(' ') + 1:]
    ok = False
    new_amount = int(option)
    for i in range(get_length(t_list)):
        if get_day(t_list[i]) == day and get_tip(t_list[i]) == tip and get_desc(t_list[i]) == desc:
            ok = True
            # t_list[i] = set_amount(t_list[i], new_amount)
            add_transaction(t_list, get_day(t_list[i]), new_amount, get_tip(t_list[i]), get_desc(t_list[i]))
            del t_list[i]
    if ok == False:
        raise ValueError("There are no such transactions")
    return t_list


def compute_day(t_list, day):
    """
    computes if the command requested is 'list balance'
    :param: day as an int
    """
    sum = int(0)
    i = int(0)
    while get_day(t_list[i]) <= day:
        if get_tip(t_list[i]) == 'in':
            sum += get_amount(t_list[i])
        else:
            sum -= get_amount(t_list[i])
        i += 1
    print("     Account’s balance at the end of day", day, "was", sum)


def condition_c(t_list, i, tip):
    """
    :return: True or False
    :param: the n th element of the list and the requested command
    """
    if tip == '': return True
    if tip[:2] == 'in' and get_tip(t_list[i]) == 'in': return True
    if tip[:3] == 'out' and get_tip(t_list[i]) == 'out': return True
    if tip[:1] == '<' and get_amount(t_list[i]) < int(tip[2:]): return True
    if tip[:1] == '>' and get_amount(t_list[i]) > int(tip[2:]): return True
    if tip[:1] == '=' and get_amount(t_list[i]) == int(tip[2:]): return True
    return False


def option_c(t_list, tip):
    """
    computes if the command requested is 'list'
    :param: the command as a string
    """
    if tip[:7] == 'balance':
        day = int(tip[8:])
        compute_day(day)
        return

    if get_length(t_list) == 0:
        print("     All transactions have been deleted")
        return
    pos = int(0)
    for i in range(get_length(t_list)):
        if condition_c(t_list, i, tip):
            pos += 1
            print(pos, '.  day: ', get_day(t_list[i]),
                  ';  amount: ', get_amount(t_list[i]),
                  ' RON;  type: ', get_tip(t_list[i]),
                  ';  description: ', get_desc(t_list[i]), sep='')


def option_d_sum(t_list, tip):
    """
    computes the total amount from in/out transactions
    :param: type of transaction
    :return: the computed sum
    """
    sum = int(0)
    tip.strip()
    for i in range(get_length(t_list)):
        if get_tip(t_list[i]) == tip[:-1]:
            sum += get_amount(t_list[i])
    if tip[:-1] == 'out':
        sum *= -1
    if tip[:-1] == 'out' or tip[:-1] == 'in':
        return tip, sum
    else:
        raise ValueError("Invalid type. Transactions can only be 'in' or 'out'")


def option_d_max(t_list, option):
    """
    displays the maximum out transaction on a day
    :param: type of transaction
    """
    tip = option[:option.find(' ')]
    option = option[option.find(' ') + 1:]
    day = int(option[:option.find(' ')])
    sum = int(0)

    for i in range(get_length(t_list)):
        if tip == get_tip(t_list[i]) and day == get_day(t_list[i]):
            sum += get_amount(t_list[i])
    if tip == 'out' or tip == 'in':
        return tip, day, sum
    else:
        raise ValueError("Invalid type. Transactions can only be 'in' or 'out'")


def option_e(t_list, option):
    """
    only keeps transactions which a rule depending on 'option'
    :param: type of transaction
    :return: new filtered list
    """
    tip = option[:option.find(' ')]
    option = option[option.find(' ') + 1:]
    if tip != 'out' and tip != 'in':
        raise ValueError("Invalid type. Transactions can only be 'in' or 'out'")
    if option == '':
        pos = int(0)
        for i in range(get_length(t_list)):
            if not get_tip(t_list[pos]) == tip:
                del t_list[pos]
                pos -= 1
            pos += 1
        return t_list
    else:
        amount = int(option[:option.find(' ')])
        pos = int(0)
        for i in range(get_length(t_list)):
            if not (get_tip(t_list[pos]) == tip and get_amount(t_list[pos]) < amount):
                del t_list[pos]
                pos -= 1
            pos += 1
        return t_list
