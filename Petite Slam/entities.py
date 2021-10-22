from dataclasses import dataclass


@dataclass
class Player:
    __id: int
    __name: str
    __strength: int

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def strength(self):
        return self.__strength

    def inc_str(self):
        self.__strength += 1

    def __str__(self):
        return 'ID: ' + str(self.__id) + '     Name: ' + self.__name + '     Playing strength: ' + str(self.__strength)


def read_player_file(file_name):
    result = []
    try:
        f = open(file_name, "r")
        line = f.readline().strip()
        while len(line) > 0:
            line = line.split(",")
            result.append(Player(int(line[0]), line[1], int(line[2])))
            line = f.readline().strip()
        f.close()
    except IOError as e:
        print("An error occurred - " + str(e))
        raise e
    return result


def write_player_file(file_name, players):
    f = open(file_name, "w")
    try:
        for p in players:
            person_str = str(p.id) + "," + p.name + "," + str(p.strength) + "\n"
            f.write(person_str)
        f.close()
    except Exception as e:
        print("An error occurred - " + str(e))