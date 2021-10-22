import re

from domain.sort_filter_algorithms import gnome_sort, day_comparison, month_comparison, year_comparison, filter_list, \
    is_person, is_date
from repository import binary_repo, text_repo, inmemory_repo


class Service:
    def __init__(self):
        separator = " = "
        keys = {}
        f = open('settings.properties', 'r')
        for line in f:
            if separator in line:
                name, value = line.split(separator, 1)
                keys[name.strip()] = value.strip()
        f.close()
        if keys['repository'] == 'binary_repo':
            self.repo = binary_repo.Repository()
        elif keys['repository'] == 'text_repo':
            self.repo = text_repo.Repository()
        elif keys['repository'] == 'inmemory_repo':
            self.repo = inmemory_repo.Repository()

        self._list = []
        self.pos = -1

    def p_validator(self, id, phone_number):
        """
        Tests if the parameters for the new person are correct
        """
        # phone number
        if len(phone_number) != 10 or phone_number[:2] != '07' or not phone_number.isdigit():
            raise ValueError('      Invalid phone number!')

        # id
        for person in self.repo._persons:
            if person.id == id:
                raise ValueError('      Duplicate id!')
        if id <= 0:
            raise ValueError('      The id cannot be negative or 0!')

    def a_validator(self, act_id, pers_list, time):
        """
        Tests if the parameters for the new activity are correct
        """
        # id
        for activity in self.repo._activities:
            if activity.id == act_id:
                raise ValueError('      Duplicate id!')
        if act_id <= 0:
            raise ValueError('      The id cannot be negative or 0!')

        # person list
        for id in pers_list:
            ok = 0
            for person in self.repo._persons:
                if person.id == id:
                    ok = 1
            if ok == 0:
                raise ValueError('      Invalid person list!')
        for id in pers_list:
            nr = 0
            for id2 in pers_list:
                if id == id2:
                    nr += 1
            if nr != 1:
                raise ValueError('      Invalid person list!')

        # time
        ok = 0
        for i in range(len(time)):
            if not time[i].isdigit() and time[i] != '/':
                raise ValueError('      Invalid time!')
            if time[i] == '/':
                ok += 1
        if ok != 1:
            raise ValueError('      Invalid time!')
        if not 0 < int(time[:time.find('/')]) < 25 or not 0 < int(time[time.find('/') + 1:]) < 25 or \
                not int(time[:time.find('/')]) < int(time[time.find('/') + 1:]):
            raise ValueError('      Invalid time!')

    def a_validator_date(self, date):
        nr = 0
        for i in range(len(date)):
            if not date[i].isdigit() and date[i] != '/':
                raise ValueError('      Invalid date!')
            if date[i] == '/':
                nr += 1
        if nr != 2:
            raise ValueError('      Invalid date!')
        if not 0 < int(date[:date.find('/')]) < 29:
            raise ValueError('      Invalid date!')
        date = date[date.find('/') + 1:]
        if not 0 < int(date[:date.find('/')]) < 13:
            raise ValueError('      Invalid date!')
        if not 2019 < int(date[date.find('/') + 1:]) < 2022:
            raise ValueError('      Invalid date!')

    def a_check_persons(self, pers_list, date, time):
        """
        Tests is there is any person who has to do multiple activities at once
        """
        for i in range(len(pers_list)):
            id = int(pers_list[i])
            for activity in self.repo._activities:
                for j in range(len(activity.act_pers_list)):
                    a_h2 = int(activity.time[activity.time.find('/') + 1:])
                    a_h1 = int(activity.time[:activity.time.find('/')])
                    b_h2 = int(time[time.find('/') + 1:])
                    b_h1 = int(time[:time.find('/')])
                    if id == int(activity.act_pers_list[j]) and activity.date == date and \
                            (a_h1 < b_h2 <= a_h2 or a_h1 <= b_h1 < a_h2):
                        raise ValueError('      One person cannot have multiple activities at once.')

    def p_add(self, pers_id, name, phone_number):
        """
        Adds a new person to the list
        :param pers_id: int
        :param name: str
        :param phone_number: str
        """
        self.p_validator(pers_id, phone_number)
        self.repo.p_add(pers_id, name, phone_number)

        self.history_add(["self.repo.p_add({}, '{}', '{}')".format(pers_id, name, phone_number),
                          'self.repo.p_remove({})'.format(pers_id)])

    def p_remove(self, id):
        """
        Removes a person from the list
        :param id: int
        """
        for person in self.repo._persons:
            if person.id == id:
                self.repo.p_remove(id)
                self.history_add(['self.repo.p_remove({})'.format(id),
                                  "self.repo.p_add({}, '{}', '{}')".format(person.id, person.name,
                                                                           person.phone_number)])
                return
        raise ValueError('     Person not found.')

    def p_update(self, id, name, phone_number):
        for person in self.repo._persons:
            if person.id == id:
                old_name = person.name
                old_phone_number = person.phone_number
                self.repo.p_remove(id)
                self.p_add(id, name, phone_number)
                self.history_add(
                    ["self.repo.p_remove({})\nself.repo.p_add({},'{}','{}')".format(id, id, name, phone_number),
                     "self.repo.p_remove({})\nself.repo.p_add({},'{}','{}')".format(id, id, old_name,
                                                                                    old_phone_number)])
                return
        raise ValueError('     Person not found.')

    def p_search_name(self, name):
        persons = ''
        for person in self.repo._persons.values():
            if re.search(name, person.name, re.IGNORECASE):
                persons += str(person) + '\n'
        if not persons:
            return '      No person was found.'
        else:
            return persons

    def p_search_number(self, number):
        number = str(number)
        persons = ''
        for person in self.repo._persons:
            if re.search(number, person.phone_number, re.IGNORECASE):
                persons += str(person) + '\n'
        if not persons:
            return '      No person was found.'
        return persons

    def a_add(self, act_id, pers_list, date, time, desc):
        """
        Adds a new activity to the list
        :param act_id: int
        :param pers_list: list
        :param date: str
        :param time: str
        :param desc: str
        """
        self.a_validator(act_id, pers_list, time)
        self.a_validator_date(date)
        self.a_check_persons(pers_list, date, time)
        self.repo.a_add(act_id, pers_list, date, time, desc)

        self.history_add(["self.repo.a_add({},{},'{}','{}','{}')".format(act_id, pers_list, date, time, desc),
                          "self.repo.a_remove({})".format(act_id)])

    def a_remove(self, id):
        """
        Removes an activity
        :param id: int
        """
        for activity in self.repo._activities:
            if activity.id == id:
                self.repo.a_remove(id)
                self.history_add(["self.repo.a_remove({})".format(id),
                                  "self.repo.a_add({},{},'{}','{}','{}')".format(id, activity.act_pers_list,
                                                                                 activity.date, activity.time,
                                                                                 activity.desc)])
                return
        raise ValueError('     Activity not found.')

    def a_update(self, id, pers_list, date, time, desc):
        """
        Updates an activity with new parameters
        :param id: int
        :param pers_list: list
        :param date: str
        :param time: str
        :param desc: str
        """
        for activity in self.repo._activities:
            if activity.id == id:
                old_pers_list = activity.act_pers_list
                old_date = activity.date
                old_time = activity.time
                old_desc = activity.desc
                self.repo.a_remove(id)
                self.a_add(id, pers_list, date, time, desc)
                self.history_add(["self.repo.a_remove({})\nself.repo.a_add({},{},'{}','{}','{}')".format(id, id,
                                                                                                         pers_list,
                                                                                                         date, time,
                                                                                                         desc),
                                  "self.repo.a_remove({})\nself.repo.a_add({},{},'{}','{}','{}')".format(id, id,
                                                                                                         old_pers_list,
                                                                                                         old_date,
                                                                                                         old_time,
                                                                                                         old_desc)])
                return
        raise ValueError('     Activity not found.')

    def a_search_desc(self, desc):
        activities = ''
        for activity in self.repo._activities.values():
            if re.search(desc, activity.desc, re.IGNORECASE):
                activities += str(activity) + '\n'
        if not activities:
            raise ValueError('      No activity was found.')
        return activities

    def a_search_date(self, date, time):
        activities = ''
        for activity in self.repo._activities.values():
            if re.search(date, activity.date, re.IGNORECASE) and \
                    int(activity.time[:activity.time.find('/')]) <= int(time) <= int(activity.time[activity.time.find('/') + 1:]):
                activities += str(activity) + '\n'
        if not activities:
            raise ValueError('      No activity was found.')
        return activities

    def a_date(self, date):
        self.a_validator_date(date)
        activities = filter_list(self.repo._activities.values(), date, is_date)
        if not activities:
            raise ValueError('      No activity was found.')
        activities.sort(key=lambda activity: int(activity.time[:activity.time.find('/')]))
        return activities

    def a_sort_time(self):
        activities = self.repo._activities
        dates = {}

        for act_nr in range(len(activities.values())):
            try:
                dates[str(activities.values()[act_nr].date)] += int(
                    activities.values()[act_nr].time[:activities.values()[act_nr].time.find('/')]) - int(
                    activities.values()[act_nr].time[activities.values()[act_nr].time.find('/') + 1:])
            except:
                dates[str(activities.values()[act_nr].date)] = int(
                    activities.values()[act_nr].time[:activities.values()[act_nr].time.find('/')]) - int(
                    activities.values()[act_nr].time[activities.values()[act_nr].time.find('/') + 1:])

        gnome_sort(activities, day_comparison)
        gnome_sort(activities, month_comparison)
        gnome_sort(activities, year_comparison)

        return sorted(dates, key=dates.get, reverse=True), activities, dates

    def a_person(self, id):
        try:
            id = int(id)
            id = abs(id)
        except:
            raise ValueError('      Invalid ID!')

        return filter_list(self.repo._activities.values(), id, is_person)

    def p_all(self):
        return self.repo.p_storage()

    def a_all(self):
        return self.repo.a_storage()

    def sort_all(self):
        self.repo.p_sort()
        self.repo.a_sort()

    def history_add(self, operation):
        self._list = self._list[:self.pos + 1]
        self._list.append(operation)
        self.pos += 1

    def undo(self):
        if self.pos < 0:
            raise ValueError('There is no operation to undo.')
        exec(self._list[self.pos][1])
        self.pos -= 1

    def redo(self):
        try:
            exec(self._list[self.pos + 1][0])
            self.pos += 1
        except:
            raise ValueError('There is no operation to redo.')
