from src.domain.entity import sort_t_list
from src.functions.functions import option_a_add, option_a_insert, option_b_remove, option_b_replace, option_c, \
    add_transaction, option_d_sum, option_d_max, option_e


def set_up():
    """
    sets up all the already known transactions
    """
    t_list = []

    add_transaction(t_list, 1, 35, "out", "pizza")
    add_transaction(t_list, 4, 3500, "in", "salary")
    add_transaction(t_list, 5, 100, "out", "groceries")
    add_transaction(t_list, 16, 210, "out", "tax")
    add_transaction(t_list, 17, 120, "out", "gasoline")
    add_transaction(t_list, 19, 1000, "in", "deposit")
    add_transaction(t_list, 21, 140, "out", "groceries")
    add_transaction(t_list, 26, 23, "out", "fastfood")
    add_transaction(t_list, 26, 230, "out", "clothes")
    add_transaction(t_list, 29, 45, "out", "book")
    return t_list


def print_menu(t_list, history):
    print("\n             MENU: \n"
          "Add transaction: \n"
          "     add <value> <type> <description> \n"
          "     insert <day> <value> <type> <description> \n"
          "Modify transactions \n"
          "     remove <day> \n"
          "     remove <start day> to <end day> \n"
          "     remove <type> \n"
          "     replace <day> <type> <description> with <value> \n"
          "Display transactions having different properties \n"
          "     list \n"
          "     list <type> \n"
          "     list [ < | = | > ] <value> \n"
          "     list balance <day> \n"
          "Obtain different characteristics of the transactions \n"
          "     sum <type> \n"
          "     max <type> <day> \n"
          "Filter \n"
          "     filter <type> \n"
          "     filter <type> <value> \n"
          "Undo \n"
          "     undo \n"
          "Exit program \n"
          "     exit \n \n")

    option = str(input())
    option += ' '
    temp_op = str(option[:option.find(' ')])
    if temp_op == 'add':
        history += (tuple(t_list[:]),)
        print_menu(option_a_add(t_list, str(option[4:])), history)
        return
    elif temp_op == 'insert':
        history += (tuple(t_list),)
        print_menu(option_a_insert(t_list, str(option[7:])), history)
        return
    elif temp_op == 'remove':
        history += (tuple(t_list),)
        print_menu(option_b_remove(t_list, option[7:]), history)
        return
    elif temp_op == 'replace':
        history += (tuple(t_list),)
        print_menu(option_b_replace(t_list, str(option[8:])), history)
        return
    elif temp_op == 'list':
        sort_t_list(t_list)
        option_c(t_list, str(option[5:]))
        print_menu(t_list, history)
        return
    elif temp_op == 'sum':
        tip, sum = option_d_sum(t_list, option[4:])
        print("     All", tip, "transactions add up to", sum)
        print_menu(t_list, history)
        return
    elif temp_op == 'max':
        tip, day, sum = option_d_max(t_list, option[4:])
        print("     The maximum", tip, "transaction on day", day, "is", sum)
        print_menu(t_list, history)
        return
    elif temp_op == 'filter':
        history += (tuple(t_list),)
        print_menu(option_e(t_list, option[7:]), history)
        return
    elif temp_op == 'undo':
        if len(history) == 0:
            print("     There are no operations left to undo.")
            print_menu(t_list, history)
        else:
            print("     The last operation has been reversed!")
            print_menu(list(history[-1]), history[:-1])
            return
    elif temp_op == 'exit':
        exit('  Bye!')
    else:
        print("    The command you entered does not exist. Try again")
        print_menu(t_list, history)
