from random import randrange
import names
import os.path

from domain.sort_filter_algorithms import gnome_sort, id_comparison
from src.domain.entities import Person, Activity, write_activity_text_file, read_activity_text_file, \
    write_person_text_file, read_person_text_file
from src.domain.iterable_collection import Collection


class Repository:
    def __init__(self):
        separator = " = "
        keys = {}
        f = open('settings.properties', 'r')
        for line in f:
            if separator in line:
                name, value = line.split(separator, 1)
                keys[name.strip()] = value.strip()
        f.close()

        self.person_file = keys['persons']
        self.activities_file = keys['activities']

        if os.path.isfile(self.activities_file) and os.path.isfile(self.person_file):
            self._persons = read_person_text_file(self.person_file)
            self._activities = read_activity_text_file(self.activities_file)
        else:
            self._persons = Collection()
            self._activities = Collection()
            desc = ['football', 'homework', 'sleeping', 'gym', 'shopping', 'watching movies', 'hiking', 'jogging',
                    'studying']
            for i in range(1, 10):
                # generates random person
                name = names.get_full_name()
                id = i
                phone_number = '07'
                phone_number += str(randrange(10000000, 99999999))
                self._persons.add(Person(id, name, phone_number))

                # generates random activity
                act_pers_list = []
                random_nr = randrange(1, 5)
                for j in range(random_nr):
                    if j != 0:
                        try:
                            act_pers_list.append(randrange(act_pers_list[-1] + 1, 11))
                        except:
                            break
                    else:
                        act_pers_list.append(randrange(1, 10))
                date = str(randrange(1, 29)) + '/' + str(randrange(1, 12)) + '/' + '2020'
                time = str(randrange(1, 23))
                time += '/' + str(randrange(int(time) + 1, 25))
                self._activities.add(Activity(id, act_pers_list, date, time, desc[randrange(8)]))
            self._persons.add(Person(10, 'Rick Astley', '0740129812'))
            self._activities.add(Activity(10, [10], '23/8/2020', '12/13', 'rickrolling'))
            write_person_text_file(self.person_file, self._persons)
            write_activity_text_file(self.activities_file, self._activities)

    def p_add(self, pers_id, name, phone_number):
        self._persons.add(Person(pers_id, name, phone_number))
        write_person_text_file(self.person_file, self._persons)

    def p_remove(self, id):
        self._persons.__delitem__(id)
        write_person_text_file(self.person_file, self._persons)

    def p_storage(self):
        """
        Returns the list of current persons
        """
        return read_person_text_file(self.person_file)

    def a_add(self, act_id, pers_list, date, time, desc):
        self._activities.add(Activity(act_id, pers_list, date, time, desc))
        write_activity_text_file(self.activities_file, self._activities)

    def a_remove(self, act_id):
        self._activities.__delitem__(act_id)
        write_activity_text_file(self.activities_file, self._activities)

    def a_storage(self):
        """
        Returns the list of current activities
        """
        return read_activity_text_file(self.activities_file)

    def p_sort(self):
        """
        Sorts the persons
        """
        gnome_sort(self._persons, id_comparison)
        write_person_text_file(self.person_file, self._persons)

    def a_sort(self):
        """
        Sorts the activities
        """
        gnome_sort(self._activities, id_comparison)
        write_activity_text_file(self.activities_file, self._activities)
