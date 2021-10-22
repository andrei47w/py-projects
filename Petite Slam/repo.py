from entities import read_player_file
import math
import random


class Repo:
    def __init__(self):
        self.file_name = 'players.txt'
        self.players = read_player_file(self.file_name)

    def list(self):
        return self.players

    def play_round(self, player1, player2):
        if player1.strength > player2.strength:
            return 1
        else:
            return 2

    def generate_pairs(self, max):
        """
        Randomly generates player pairs for the next round
        :param max: amount of players that needs to be sorted
        :return: randomixed list
        """
        list = []
        for i in range(max):
            list.append(i)

        new_list = []
        for i in range(max - 1):
            player = random.randint(1, len(list) - 1)
            new_list.append(list[player])
            list.remove(list[player])
        new_list.append(list[0])

        return new_list

    def sort(self):
        self.players.sort(key=lambda player: player.strength, reverse=True)

    def play_qualifying_round(self):
        player_list = self.players
        temp_count = len(player_list)
        while not int(math.sqrt(temp_count) + 0.5) ** 2 == temp_count:
            temp_count -= 1

        random_list = self.generate_pairs(2 * (len(player_list) - temp_count))
        offset = len(player_list)-temp_count

        new_list = []
        for i in range(0, len(random_list), 2):
            if self.play_round(player_list[random_list[i]+offset], player_list[random_list[i+1]+offset]) == 1:
                player_list[random_list[i]+offset].inc_str()
                new_list.append(player_list[random_list[i]+offset])
            else:
                player_list[random_list[i+1]+offset].inc_str()
                new_list.append(player_list[random_list[i+1]+offset])

        self.players = player_list[:offset+1] + new_list

    def play_tourney(self):
        player_list = self.players
        print(len(self.players))

        index = len(self.players)
        past_list = player_list
        while index != 1:
            random_list = self.generate_pairs(len(past_list))
            new_list = []
            for i in range(0, len(random_list), 2):
                if self.play_round(player_list[random_list[i]], player_list[random_list[i+1]]) == 1:
                    player_list[random_list[i]].inc_str()
                    new_list.append(player_list[random_list[i]])
                else:
                    player_list[random_list[i+1]].inc_str()
                    new_list.append(player_list[random_list[i+1]])
            print('Round '+ math.sqrt(len(self.players)) +' : \n'+ new_list + '\n')
            pest_list = new_list
            index /= 2
