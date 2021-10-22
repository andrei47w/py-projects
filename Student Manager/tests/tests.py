import re
import unittest

from domain.entities import Person
from repository import inmemory_repo
from repository import text_repo
from repository import binary_repo
from service.service import Service
from src.domain.iterable_collection import Collection

f = open('settings.properties', 'w')
f.write('repository = inmemory_repo\npersons = inmemory\nactivities = inmemory\nui = GUI')
f.close()

class TestPersonMethods(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.repo = inmemory_repo.Repository()
        self.repo._persons = Collection()

    def test_list1(self):
        self.assertTrue(
            re.search("Person__id=10, _Person__name='Rick Astley', _Person__phone_number='0740129812'",
                      str(self.service.p_all().values())))
        self.assertIsNone(re.search("_Person__pers_id=11", str(self.service.p_all())))

        self.repo = inmemory_repo.Repository()
        self.assertIsNone(re.search("_Person__pers_id=10, _Person__name='Rick Astley', _Person__phone_number='0740129812'", str(self.repo.p_storage().values())))
        self.assertIsNone(re.search("_Person__pers_id=11", str(self.repo.p_storage())))

    def test_add(self):
        self.repo._persons.__setitem__(1, Person(1, 'Name', '0740128912'))
        self.service.p_add(11, 'Name', '0740219821')
        self.assertRaises(ValueError, self.service.p_add, 1, 'Name', '071234567')
        self.assertRaises(ValueError, self.service.p_add, 12, 'Name', '072345678')
        self.assertRaises(ValueError, self.service.p_add, 12, 'Name', '7712345678')
        self.assertRaises(ValueError, self.service.p_add, 12, 'Name', '07123a3x78')
        self.assertTrue(self.repo._persons.values()[0].id == 1)
        self.assertTrue(self.repo._persons.values()[0].name == 'Name')
        self.assertTrue(self.repo._persons.values()[0].phone_number == '0740128912')
        self.assertRaises(ValueError, self.service.p_add, -12, 'Name', '0712345678')

    def test_update(self):
        self.repo.p_add(1, 'Name', '0740219821')
        self.service.p_update(1, 'Name', '0740219821')
        self.repo.p_remove(1)
        self.repo.p_add(1, 'Name2', '0700000000')
        if self.repo._persons.values()[0].name != 'Name2' or self.repo._persons.values()[0].phone_number != '0700000000':
            raise ValueError("Failed to update a person!")
        self.assertRaises(ValueError, self.service.p_update, 12, 'Name3', '0712345678')

    def test_remove(self):
        self.repo.p_add(1, 'Name', '0740219821')
        self.service.p_remove(2)
        self.repo.p_remove(1)
        self.assertFalse(self.repo._persons == [])
        self.assertRaises(ValueError, self.service.p_remove, 12)
        self.assertRaises(ValueError, self.service.p_remove, 112)

    def test_search(self):
        self.assertTrue(re.search('10                 Rick Astley                  0740129812',
                                  str(self.service.p_search_name('Rick'))))
        self.assertTrue(re.search('10                 Rick Astley                  0740129812',
                                  str(self.service.p_search_name('rick'))))
        self.assertTrue(re.search('10                 Rick Astley                  0740129812',
                                  str(self.service.p_search_name('ck'))))
        self.assertIsNone(re.search('10                 Rick Astley                  0740129812',
                                    str(self.service.p_search_name('1234qwerty'))))
        self.assertTrue(re.search('10                 Rick Astley                  0740129812',
                                  str(self.service.p_search_number('0740129812'))))
        self.assertTrue(re.search('10                 Rick Astley                  0740129812',
                                  str(self.service.p_search_number('0740'))))
        self.assertTrue(re.search('10                 Rick Astley                  0740129812',
                                  str(self.service.p_search_number('74'))))
        self.assertIsNone(re.search('10                 Rick Astley                  0740129812',
                                    str(self.service.p_search_number('1234qwerty'))))
    def test_list2(self):
        self.repo.p_add(1, 'Name', '0740219821')
        printed_str = ''
        for person in self.repo._persons.__iter__():
            printed_str += str(person)
        print(printed_str)
        self.assertTrue(re.search('1                  Name                         0740219821', str(printed_str)))

class TestActivityMethods(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.repo = inmemory_repo.Repository()
        self.repo._activities = Collection()

    def test_list(self):
        self.assertTrue(re.search(", _Activity__date='23/8/2020', _Activity__time='12/13', _Activity__desc='rickrolling'", str(self.service.a_all().values())))
        self.assertRaises(TypeError, str(self.service.a_all().values()))
        self.assertIsNone(re.search("_Activity__act_id=11", str(self.service.a_all().values())))

        self.repo = inmemory_repo.Repository()
        self.assertTrue(re.search(", _Activity__date='23/8/2020', _Activity__time='12/13', _Activity__desc='rickrolling'", str(self.repo.a_storage().values())))
        self.assertIsNone(re.search("_Activity__act_id=10, _Activity__pers_list=", str(self.repo.a_storage().values())))
        self.assertIsNone(re.search("_Activity__act_id=11", str(self.repo.a_storage().values())))

    def test_add(self):
        self.repo.p_add(1, 'Name', '0740219821')
        self.repo.a_add(1, [1], '11/11/2020', '11/12', 'desc')
        self.service.a_add(11, [1], '11/11/2020', '11/12', 'desc')
        self.assertTrue(self.repo._activities.values()[0].id == 1)
        self.assertTrue(self.repo._activities.values()[0].act_pers_list == [1])
        self.assertTrue(self.repo._activities.values()[0].date == '11/11/2020')
        self.assertTrue(self.repo._activities.values()[0].time == '11/12')
        self.assertTrue(self.repo._activities.values()[0].desc == 'desc')
        self.assertRaises(ValueError, self.service.a_add, 1, [1], '11/11/2020', '12/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/2020', '12/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/2020', '32/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/2020', '12/62', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/2020', '111', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/2020', '1x/a1', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/c1/2er0', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [12], '11/11/2020', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11112020', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1, 1], '11/11/2020', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/2020', '14/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '51/11/2020', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/51/2020', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, 12, [1], '11/11/20', '11/13', 'desc')
        self.assertRaises(ValueError, self.service.a_add, -12, [1], '11/11/20', '11/13', 'desc')

    def test_multiple_activities(self):
        self.repo.p_add(2, 'Name', '0740219821')
        self.repo.a_add(1, [2], '6/7/2020', '4/8', 'desc')
        self.service.a_check_persons([2], '6/7/2020', '2/3')
        self.assertRaises(ValueError, self.service.a_add, 2, [2], '6/7/2020', '4/9', 'desc')

    def test_update(self):
        self.repo.p_add(1, 'Name', '0740219821')
        self.repo.a_add(1, [1], '6/7/2020', '4/8', 'desc')
        self.service.a_update(1, [1], '6/7/2020', '4/8', 'desc')
        self.repo.a_remove(1)
        self.repo.a_add(1, [1], '6/7/2021', '1/2', 'desc2')
        if self.repo._activities.values()[0].date != '6/7/2021' or \
                self.repo._activities.values()[0].time != '1/2' or \
                self.repo._activities.values()[0].desc != 'desc2':
            raise ValueError("Failed to update an activity!")

    def test_remove(self):
        self.repo.p_add(2, 'Name', '0740219821')
        self.repo.a_add(1, [2], '6/7/2020', '4/8', 'desc')
        self.service.a_remove(2)
        self.repo.a_remove(1)
        if self.repo._activities:
            raise ValueError("Failed to remove an activity by id!")
        self.repo.a_add(1, [2], '6/7/2020', '4/8', 'desc')
        self.assertRaises(ValueError, self.service.a_remove, self.repo._activities[0])

    def test_search(self):
        self.assertTrue(re.search('               23/8/2020          12:00 -> 13:00     rickrolling',
                                  str(self.service.a_search_desc('rick'))))
        self.assertTrue(re.search('               23/8/2020          12:00 -> 13:00     rickrolling',
                                  str(self.service.a_search_desc('Rick'))))
        self.assertTrue(re.search('               23/8/2020          12:00 -> 13:00     rickrolling',
                                  str(self.service.a_search_desc('rickrolling'))))
        self.assertTrue(re.search('               23/8/2020          12:00 -> 13:00     rickrolling',
                                  str(self.service.a_search_desc('g'))))
        self.assertRaises(ValueError, self.service.a_search_desc, '1234qwerty')
        self.assertTrue(re.search('               23/8/2020          12:00 -> 13:00     rickrolling',
                                  str(self.service.a_search_date('23/8/2020', '12'))))
        self.assertRaises(ValueError, self.service.a_search_date, '23/8/2020', '')
        self.assertRaises(ValueError, self.service.a_search_date, '2', '')
        self.assertTrue(re.search('               23/8/2020          12:00 -> 13:00     rickrolling',
                                  str(self.service.a_search_date('23/8/2020', '13'))))
        self.assertRaises(ValueError, self.service.a_search_date, '1234qwerty', '')


class TestOtherMethods(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.repo = inmemory_repo.Repository()
        self.repo._activities = Collection()

    def test_act_date(self):
        self.assertTrue(
            re.search(" _Activity__date='23/8/2020', _Activity__time='12/13', _Activity__desc='rickrolling'",
                      str(self.service.a_date('23/8/2020'))))
        self.assertRaises(ValueError, self.service.a_date, '1234qwerty')
        self.assertRaises(ValueError, self.service.a_date, '23')

    def test_act_sort(self):
        self.assertTrue(re.search("'23/8/2020'", str(self.service.a_sort_time())))
        self.assertIsNone(re.search("_Activity__act_id=10", str(self.service.a_sort_time())))
        self.assertIsNone(re.search("_Activity__pers_list=", str(self.service.a_sort_time())))
        self.assertIsNone(re.search("_Activity__time='12/13'", str(self.service.a_sort_time())))
        self.assertIsNone(re.search("_Activity__desc='rickrolling'", str(self.service.a_sort_time())))

    def test_act_person(self):
        self.assertIsNone(re.search("               23/8/2020          12:00 -> 13:00     rickrolling",
                                  str(self.service.a_person('10'))))
        self.assertIsNone(re.search("               23/8/2020          12:00 -> 13:00     rickrolling",
                                    str(self.service.a_person('1'))))
        self.assertRaises(ValueError, self.service.a_person, 'O')
        self.assertRaises(ValueError, self.service.a_person, 'x')

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.repo = inmemory_repo.Repository()
        self.repo._activities = Collection()
        self.repo._persons = Collection()

    def test_persons(self):
        self.service.p_add(11, 'Name', '0740219821')
        self.service.undo()
        self.assertRaises(ValueError, self.service.undo)
        self.service.redo()
        self.assertRaises(ValueError, self.service.redo)

        self.service.p_remove(11)
        self.service.undo()
        self.service.undo()
        self.assertRaises(ValueError, self.service.undo)
        self.service.redo()
        self.service.redo()
        self.assertRaises(ValueError, self.service.redo)

        self.service.p_add(11, 'Name', '0740219821')
        self.service.undo()
        self.service.undo()
        self.service.undo()
        self.assertRaises(ValueError, self.service.undo)
        self.service.redo()
        self.service.redo()
        self.service.redo()
        self.assertRaises(ValueError, self.service.redo)
        self.assertTrue(len(self.service._list) == 3)

    def test_activities(self):
        self.service.p_add(11, 'Name', '0740219821')
        self.service._list = []
        self.service.pos = -1
        self.service.a_add(11, [11], '11/11/2020', '11/12', 'desc')
        self.service.undo()
        self.assertRaises(ValueError, self.service.undo)
        self.service.redo()
        self.assertRaises(ValueError, self.service.redo)

        self.service.a_remove(11)
        self.service.undo()
        self.service.undo()
        self.assertRaises(ValueError, self.service.undo)
        self.service.redo()
        self.service.redo()
        self.assertRaises(ValueError, self.service.redo)

        self.service.a_update(10, [11], '11/11/2020', '11/12', 'desc')
        self.service.undo()
        self.service.undo()
        self.service.undo()
        self.service.undo()
        self.assertRaises(ValueError, self.service.undo)
        self.service.redo()
        self.service.redo()
        self.service.redo()
        self.service.redo()
        self.assertRaises(ValueError, self.service.redo)
        self.assertTrue(len(self.service._list) == 4)


if __name__ == '__main__':
    unittest.main()
