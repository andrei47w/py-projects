import re

from service.service import Service


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class UI:
    def __init__(self):
        self._service = Service()

    def show_menu(self):
        """
        Prints menu
        """
        print(
            bcolors.BOLD + "\n\n______________________________________________________________________________________________________________________________"
                           "\n       Menu:\n"
                           "pers_add <id> <name> <phone number>                              :adds a new person to the list\n"
                           "pers_remove <id>                                                 :removes person with the specified id\n"
                           "pers_list                                                        :lists all persons\n"
                           "pers_update <id> <name> <phone number>                           :updates the person with th e specified id\n"
                           "pers_search <name/phone number>                                  :searches the person list by name/phone number\n\n"
                           "act_add <id> <person list> <dd/mm/yyyy> <hh/hh> <description>    :adds a new activity to the list\n"
                           "act_remove <id>                                                  :removes activity with th e specified id\n"
                           "act_list                                                         :lists all activities\n"
                           "act_update <id> <person list> <dd/mm/yyyy> <hh/hh> <description> :updates the activity with th e specified id\n\n"
                           "act_search <date> <time>                                         :searches the activity list by date and time\n"
                           "act_search <desc>                                                :searches the activity list by description\n"
                           "act_date <date>                                                  :sorts all the activities on <date> by their starting time\n"
                           "act_sort                                                         :sorts all dates with activities by their free time\n"
                           "act_person <id>                                                  :lists all activities of person <id>\n\n"
                           "exit                                                             :exits the program\n"
                           "------------------------------------------------------------------------------------------------------------------------------")

    def pers_add(self, cmd):
        pers_id = int(cmd[:cmd.find(' ')])
        cmd = cmd[cmd.find(' ') + 1:]
        name = cmd[:cmd.find(' 07')]
        phone_number = cmd[cmd.find(' 07') + 1:]
        self._service.p_add(pers_id, name, phone_number)

    def pers_remove(self, cmd):
        self._service.p_remove(int(cmd))

    def pers_update(self, cmd):
        pers_id = int(cmd[:cmd.find(' ')])
        cmd = cmd[cmd.find(' ') + 1:]
        name = cmd[:cmd.find(' 07')]
        phone_number = cmd[cmd.find(' 07') + 1:]
        self._service.p_update(pers_id, name, phone_number)

    def pers_list(self):
        person_list = self._service.p_all()
        for person in person_list:
            print(str(person))

    def act_list(self):
        activity_list = self._service.a_all()
        for activity in activity_list:
            print(str(activity))

    def act_add(self, cmd):
        act_id = int(cmd[:cmd.find(' ')])
        cmd = cmd[cmd.find(' ') + 1:]
        pers_list = str(cmd[cmd.find('['):cmd.find(']') + 1])
        p_list = eval(pers_list)
        cmd = cmd[cmd.find('] ') + 2:]
        date = cmd[:cmd.find(' ')]
        cmd = cmd[cmd.find(' ') + 1:]
        time = cmd[:cmd.find(' ')]
        desc = cmd[cmd.find(' ') + 1:]
        self._service.a_add(act_id, p_list, date, time, desc)

    def act_remove(self, cmd):
        self._service.a_remove(int(cmd))

    def act_update(self, cmd):
        act_id = int(cmd[:cmd.find(' ')])
        cmd = cmd[cmd.find(' ') + 1:]
        pers_list = str(cmd[cmd.find('['):cmd.find(']') + 1])
        p_list = eval(pers_list)
        cmd = cmd[cmd.find('] ') + 2:]
        date = cmd[:cmd.find(' ')]
        cmd = cmd[cmd.find(' ') + 1:]
        time = cmd[:cmd.find(' ')]
        desc = cmd[cmd.find(' ') + 1:]
        self._service.a_update(act_id, p_list, date, time, desc)

    def pers_search(self, cmd):
        try:
            cmd = int(cmd)
        except:
            print(self._service.p_search_name(str(cmd)))
            return
        print(self._service.p_search_number(cmd))

    def act_search(self, cmd):
        if re.search('[a-zA-Z]', cmd):
            print(self._service.a_search_desc(cmd))
        else:
            print(self._service.a_search_date(cmd[:cmd.find(' ')], cmd[cmd.find(' ') + 1:]))

    def act_date(self, date):
        activities = self._service.a_date(date)
        for activity in activities:
            print(activity)

    def act_sort_time(self):
        dates = self._service.a_sort_time()[0]
        date_dict = self._service.a_sort_time()[2]
        activities = self._service.a_sort_time()[1]
        for key in dates:
            print('     ', key, '(', 24 + date_dict[key], 'free hours ):')
            for activity in activities:
                if key == activity.date:
                    print(str(activity))

    def act_person(self, cmd):
        print(self._service.a_person(cmd))

    def read_input(self):
        cmd = input(bcolors.UNDERLINE + 'Enter command' + bcolors.ENDC + ': ')
        if cmd[:4] == 'exit':
            exit('  Bye!')
        elif cmd[:9] == 'pers_add ':
            self.pers_add(cmd[9:])
        elif cmd[:12] == 'pers_remove ':
            self.pers_remove(cmd[12:])
        elif cmd[:9] == 'pers_list':
            self.pers_list()
        elif cmd[:12] == 'pers_update ':
            self.pers_update(cmd[12:])
        elif cmd[:9] == 'act_list':
            self.act_list()
        elif cmd[:8] == 'act_add ':
            self.act_add(cmd[8:])
        elif cmd[:11] == 'act_remove ':
            self.act_remove(cmd[11:])
        elif cmd[:11] == 'act_update ':
            self.act_update(cmd[11:])
        elif cmd[:12] == 'pers_search ':
            self.pers_search(cmd[12:])
        elif cmd[:11] == 'act_search ':
            self.act_search(cmd[11:])
        elif cmd[:9] == 'act_date ':
            self.act_date(cmd[9:])
        elif cmd[:8] == 'act_sort':
            self.act_sort_time()
        elif cmd[:11] == 'act_person ':
            self.act_person(cmd[11:])
        else:
            print(bcolors.WARNING + '     Unknown command!' + bcolors.ENDC)

    def start(self):
        while True:
            try:
                self.show_menu()
                self.read_input()
                self._service.sort_all()
            except ValueError as ve:
                print(bcolors.WARNING + str(ve) + bcolors.ENDC)
