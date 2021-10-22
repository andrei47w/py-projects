def get_length(transactions):
    return len(transactions)


def get_day(transaction):
    return transaction[0]


def get_amount(transaction):
    return transaction[1]


def get_tip(transaction):
    return transaction[2]


def get_desc(transaction):
    return transaction[3]


def sort_t_list(transactions):
    transactions.sort(reverse=False, key=lambda transaction: transaction[0])
    return transactions


def set_amount(transactions, new_amount):
    transactions[1] = new_amount
    return transactions


def set_transaction(transactions, new_transaction):
    transactions.append(new_transaction)
    return transactions
