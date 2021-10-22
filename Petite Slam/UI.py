from entities import read_player_file
from repo import Repo


class UI:
    def __init__(self):
        self.repo = Repo()

    def list_players(self):
        for player in self.repo.list():
            print(str(player))

    def start(self):
        self.repo.sort()
        self.list_players()
        print('\nRemaining players after the qualifying round: ')
        self.repo.play_qualifying_round()
        self.repo.sort()
        self.list_players()
        # self.repo.play_tourney()
