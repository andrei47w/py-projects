class Collection:
    class Iterator:
        def __init__(self, collection):
            self.__collection = collection

            self.__id_iterator = iter(self.__collection._data)

        def __iter__(self):
            return self

        def __next__(self):
            return self.__collection._data[next(self.__id_iterator)]

    def __init__(self):
        self._data = {}

    def __iter__(self):
        return Collection.Iterator(self)

    def __getitem__(self, key):
        return self._data[key] if key in self._data else None

    def __setitem__(self, id, entity):
        self._data[id] = entity

    def __delitem__(self, key):
        del self._data[key]

    def __len__(self):
        return len(self._data)

    def values(self):
        return list(self._data.values())

    def add(self, entity):
        self._data[entity.id] = entity

    def reorder(self, new_order):
        self._data = {k: self._data[k] for k in new_order}

# c = Collection()
# c.add(Person(2, 'name2', 'number'))
# c.add(Person(3, 'name3', 'number'))
# c.add(Person(4, 'name4', 'number'))
# c.add(Person(5, 'name5', 'number'))
# c.add(Person(1, 'name1', 'number'))
# c.add(Person(6, 'name6', 'number'))
#
# print(c._data)
# for person in c:
#     print(person)
# gnome_sort(c, id_comparison)
# for person in c:
#     print(person)
