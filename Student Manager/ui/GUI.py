from tkinter import *
from tkinter import messagebox

from service.service import Service


class GUI:
    def __init__(self, ctr):
        self.frame = None
        self.tk = Tk()
        self.service = Service()
        self.ctrl = ctr

    def start(self):
        self.tk.title("Activity App")

        frame = Frame(self.tk)
        frame.pack()
        self.frame = frame
        frame.configure(background="#3C3F41")

        l1 = Label(frame, text='ID:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=0, column=0)
        l1 = Label(frame, text='Name:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=0, column=2)
        l1 = Label(frame, text='Phone Number:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=0, column=4)
        l1 = Label(frame, text='ID:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=1, column=0)
        l1 = Label(frame, text='Person List:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=1, column=2)
        l1 = Label(frame, text='Date:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=1, column=4)
        l1 = Label(frame, text='Time:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=1, column=6)
        l1 = Label(frame, text='Description:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=1, column=8)
        l1 = Label(frame, text='Remove ID:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=2, column=8)
        l1 = Label(frame, text='Search:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=3, column=8)
        l1 = Label(frame,
                   text='Activities can be searched by <dd/mm/yyyy h> or <description>\nPersons can be searched by <phone_number> or <id>',
                   bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=4, column=8, columnspan=4, rowspan=2)
        l1 = Label(frame, text='Date:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=6, column=8)
        l1 = Label(frame, text='Person:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11')
        l1.grid(row=7, column=8)

        self.pers_id = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.pers_id.grid(row=0, column=1)
        self.name = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.name.grid(row=0, column=3)
        self.phone_number = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.phone_number.grid(row=0, column=5)
        self.act_id = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.act_id.grid(row=1, column=1)
        self.pers_list = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.pers_list.grid(row=1, column=3)
        self.date = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.date.grid(row=1, column=5)
        self.time = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.time.grid(row=1, column=7)
        self.desc = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.desc.grid(row=1, column=9)
        self.remove_id = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.remove_id.grid(row=2, column=9)
        self.search_text = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.search_text.grid(row=3, column=9)
        self.sort_date = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11', width=36)
        self.sort_date.grid(row=6, column=9, columnspan=2)
        self.sort_person = Entry(frame, {}, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11', width=36)
        self.sort_person.grid(row=7, column=9, columnspan=2)

        self.list1 = Listbox(frame, height=15, width=118, bg='#2B2B2B', fg="#BBBBBB", font='Consolas 11')
        self.list1.grid(row=2, column=0, rowspan=7, columnspan=8)

        # sb1 = Scrollbar(frame)
        # sb1.grid(row=2, column=9, rowspan=15)

        # self.list1.configure(yscrollcommand=sb1.set)
        # sb1.configure(command=self.list1.yview)

        self.p_list_btn = Button(frame, text='View Persons', width=17, command=self._list_pers, bg="#3C3F41",
                                 fg="#BBBBBB", font='Consolas 11')
        self.p_list_btn.grid(row=8, column=9, sticky='SW')
        self.a_list_btn = Button(frame, text='View Activities', width=17, command=self._list_act, bg="#3C3F41",
                                 fg="#BBBBBB", font='Consolas 11')
        self.a_list_btn.grid(row=8, column=9, columnspan=2, sticky='SE')
        self.p_add_btn = Button(frame, text='Add Person', width=15, command=self._p_add, bg="#3C3F41", fg="#BBBBBB",
                                font='Consolas 11')
        self.p_add_btn.grid(row=0, column=10)
        self.a_add_btn = Button(frame, text='Add Activity', width=15, command=self._a_add, bg="#3C3F41", fg="#BBBBBB",
                                font='Consolas 11')
        self.a_add_btn.grid(row=1, column=10)
        self.p_update_btn = Button(frame, text='Update Person', width=18, command=self._p_update, bg="#3C3F41",
                                   fg="#BBBBBB", font='Consolas 11')
        self.p_update_btn.grid(row=0, column=11)
        self.a_update_btn = Button(frame, text='Update Activity', width=18, command=self._a_update, bg="#3C3F41",
                                   fg="#BBBBBB", font='Consolas 11')
        self.a_update_btn.grid(row=1, column=11)
        self.p_remove_btn = Button(frame, text='Remove Person', width=15, command=self._p_remove, bg="#3C3F41",
                                   fg="#BBBBBB", font='Consolas 11')
        self.p_remove_btn.grid(row=2, column=10)
        self.a_remove_btn = Button(frame, text='Remove Activity', width=18, command=self._a_remove, bg="#3C3F41",
                                   fg="#BBBBBB", font='Consolas 11')
        self.a_remove_btn.grid(row=2, column=11)
        self.p_search_btn = Button(frame, text='Search Person', width=15, command=self._p_search, bg="#3C3F41",
                                   fg="#BBBBBB", font='Consolas 11')
        self.p_search_btn.grid(row=3, column=10)
        self.a_search_btn = Button(frame, text='Search Activity', width=18, command=self._a_search, bg="#3C3F41",
                                   fg="#BBBBBB", font='Consolas 11')
        self.a_search_btn.grid(row=3, column=11)
        self.sort_time_btn = Button(frame, text='Filter Date', width=18, command=self._sort_time, bg="#3C3F41",
                                    fg="#BBBBBB", font='Consolas 11')
        self.sort_time_btn.grid(row=6, column=11)
        self.sort_person_btn = Button(frame, text='Filter Person', width=18, command=self._sort_person, bg="#3C3F41",
                                      fg="#BBBBBB", font='Consolas 11')
        self.sort_person_btn.grid(row=7, column=11)
        self.sort_all_btn = Button(frame, text='Sort By Free time', width=18, command=self._sort_all, bg="#3C3F41", fg="#BBBBBB",
                                   font='Consolas 11')
        self.sort_all_btn.grid(row=8, column=11, sticky='S')
        self.undo_btn = Button(frame, text='Undo', width=5, command=self._undo, bg="#3C3F41", fg="#BBBBBB",
                               font='Consolas 11')
        self.undo_btn.grid(row=8, column=8, sticky='SW')
        self.redo_btn = Button(frame, text='Redo', width=5, command=self._redo, bg="#3C3F41", fg="#BBBBBB",
                               font='Consolas 11')
        self.redo_btn.grid(row=8, column=8, sticky='SE')

        self.tk.mainloop()

    def _list_act(self):
        self.service.sort_all()
        self.list1.delete(0, 9999)
        txt = "ID                 Person List          Date                 Time               Description" + '\n'
        self.list1.insert(1, txt)
        self.list1.insert(1,
                          '----------------------------------------------------------------------------------------------------------------------')
        act_list = self.service.a_all()
        i = 2
        for activity in act_list:
            i += 1
            txt = str(activity) + '\n'
            self.list1.insert(i, txt)

    def _list_pers(self):
        self.service.sort_all()
        self.list1.delete(0, 9999)
        txt = 'ID                    Name                      Phone Number'
        self.list1.insert(1, txt)
        self.list1.insert(1,
                          '----------------------------------------------------------------------------------------------------------------------')
        person_list = self.service.p_all()
        i = 2
        for person in person_list:
            i += 1
            txt = str(person) + '\n'
            self.list1.insert(i, txt)

    def _p_add(self):
        try:
            self.service.p_add(int(self.pers_id.get()), self.name.get(), self.phone_number.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _a_add(self):
        try:
            p_list = eval(str(self.pers_list.get()))
            self.service.a_add(int(self.act_id.get()), p_list, self.date.get(), self.time.get(), self.desc.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _p_update(self):
        try:
            self.service.p_update(int(self.pers_id.get()), self.name.get(), self.phone_number.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _a_update(self):
        try:
            p_list = eval(str(self.pers_list.get()))
            self.service.a_update(int(self.act_id.get()), p_list, self.date.get(), self.time.get(), self.desc.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _p_remove(self):
        try:
            self.service.p_remove(int(self.remove_id.get()))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _a_remove(self):
        try:
            self.service.a_remove(int(self.remove_id.get()))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _p_search(self):
        try:
            self.service.sort_all()
            self.list1.delete(0, 9999)
            txt = 'ID                    Name                      Phone Number'
            self.list1.insert(1, txt)
            self.list1.insert(1,
                              '----------------------------------------------------------------------------------------------------------------------')
            try:
                cmd = int(self.search_text.get())
            except:
                person_list = self.service.p_search_name(self.search_text.get())
                if person_list and person_list[0] == ' ':
                    raise ValueError(person_list)
                while person_list:
                    self.list1.insert(END, person_list[:person_list.find('\n')])
                    person_list = person_list[person_list.find('\n') + 1:]
                return
            person_list = self.service.p_search_number(int(self.search_text.get()))
            if person_list and person_list[0] == ' ':
                raise ValueError(person_list)
            while person_list:
                self.list1.insert(END, person_list[:person_list.find('\n')])
                person_list = person_list[person_list.find('\n') + 1:]
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _a_search(self):
        try:
            self.service.sort_all()
            self.list1.delete(0, 9999)
            txt = 'ID                    Name                      Phone Number'
            self.list1.insert(1, txt)
            self.list1.insert(1,
                              '----------------------------------------------------------------------------------------------------------------------')
            cmd = self.search_text.get()
            if re.search('[a-zA-Z]', cmd):
                act_list = self.service.a_search_desc(cmd)
                if act_list and act_list[0] == ' ':
                    raise ValueError(act_list)
                while act_list:
                    self.list1.insert(END, act_list[:act_list.find('\n')])
                    act_list = act_list[act_list.find('\n') + 1:]
                return
            else:
                act_list = self.service.a_search_date(cmd[:cmd.find(' ')], cmd[cmd.find(' ') + 1:])
                if act_list and act_list[0] == ' ':
                    raise ValueError(act_list)
                while act_list:
                    self.list1.insert(END, act_list[:act_list.find('\n')])
                    act_list = act_list[act_list.find('\n') + 1:]
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _sort_person(self):
        try:
            self.service.sort_all()
            self.list1.delete(0, 9999)
            txt = "ID                 Person List          Date                 Time               Description" + '\n'
            self.list1.insert(1, txt)
            self.list1.insert(1,
                              '----------------------------------------------------------------------------------------------------------------------')
            act_list = self.service.a_person(self.sort_person.get())
            person_list = ''
            for activity in act_list:
                person_list += str(activity) + '\n'
            while person_list:
                self.list1.insert(END, person_list[:person_list.find('\n')])
                person_list = person_list[person_list.find('\n') + 1:]
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _sort_time(self):
        try:
            self.service.sort_all()
            self.list1.delete(0, 9999)
            txt = "ID                 Person List          Date                 Time               Description" + '\n'
            self.list1.insert(1, txt)
            self.list1.insert(1,
                              '----------------------------------------------------------------------------------------------------------------------')
            activities = self.service.a_date(self.sort_date.get())
            for activity in activities:
                self.list1.insert(END, str(activity))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _sort_all(self):
        try:
            self.service.sort_all()
            self.list1.delete(0, 9999)
            txt = "ID                 Person List          Date                 Time               Description" + '\n'
            self.list1.insert(1, txt)
            self.list1.insert(1,
                              '----------------------------------------------------------------------------------------------------------------------')
            dates = self.service.a_sort_time()[0]
            date_dict = self.service.a_sort_time()[2]
            activities = self.service.a_sort_time()[1]
            for key in dates:
                string = '   - ' + key + ' (' + str(24 + date_dict[key]) + ' free hours):'
                self.list1.insert(END, '')
                self.list1.insert(END, string)
                for activity in activities:
                    if key == activity.date:
                        self.list1.insert(END, str(activity))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _undo(self):
        try:
            self.service.undo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _redo(self):
        try:
            self.service.redo()
        except Exception as e:
            messagebox.showerror("Error", str(e))