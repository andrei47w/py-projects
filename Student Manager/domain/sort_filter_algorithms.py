def is_person(activity, person):
    return str(person) in activity.act_pers_list

def is_date(activity, date):
    return activity.date == date

def filter_list(item_list, condition, acceptance_function=lambda x: True):
    return [item for item in item_list if acceptance_function(item, condition)]


def id_comparison(x, y):
    return x.id < y.id

def day_comparison(x, y):
    return int(x.date[:x.date.find('/')]) < int(y.date[:y.date.find('/')])

def month_comparison(x, y):
    return int(x.date[x.date.find('/') + 1:x.date.find('/', 3)]) < int(y.date[y.date.find('/') + 1:y.date.find('/', 3)])

def year_comparison(x,y):
    return int(x.date[x.date.find('/', 3) + 1:]) < int(y.date[y.date.find('/', 3) + 1:])


def gnome_sort(entity_list, compare_function):
    list = entity_list.values()
    for pos in range(1, len(list)):
        while compare_function(list[pos], list[pos - 1]) and pos != 0:
            list[pos], list[pos-1] = list[pos-1], list[pos]
            pos -= 1
    new_order = []
    for elem in list:
        new_order.append(elem.id)
    entity_list.reorder(new_order)