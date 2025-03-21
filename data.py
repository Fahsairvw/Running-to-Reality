import csv
import os


class SaveFile:
    def __init__(self):
        if not os.path.exists("game_results.csv"):
            with open("game_results.csv", "w", newline="") as f:
                self.__writer = csv.writer(f)
                self.__writer.writerow(["Total Jump", "Score", "Level", "Time Played", "Final Speed", "Theme"])

    def add_data(self, game_list: list):
        with open("game_results.csv", "a", newline="") as f:
            self.__writer = csv.writer(f)
            self.__writer.writerow(game_list)
