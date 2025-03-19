import time
import pygame as pg
import numpy as np
from data import SaveFile
from game_component import Runner, Obstacle, Drawer
from config import Config



class SoundEffects:
    __instance = None

    def __init__(self):
        if SoundEffects.__instance is None:
            pg.mixer.init(frequency=44100, channels=2)
            self.__instance = self
            print("Sound Effects Initialized")
            self.__effects = {"jump": self.__gen_sound(0.15, 500),
                              "start": self.__gen_sound(0.15, 1200),
                              "over": self.__gen_sound(1.0, 200),
                              }
        else:
            raise Exception("This class is a singleton!")

    @staticmethod
    def get_instance():
        if SoundEffects.__instance is None:
            SoundEffects.__instance = SoundEffects()
        return SoundEffects.__instance

    @staticmethod
    def __gen_sound(duration, f, sample_rate=44100):
        t = np.arange(0, duration, 1 / sample_rate)  # x-axis
        wave = np.sin(2 * np.pi * f * t)  # y-axis

        bit = 16
        amp = 2 ** (bit - 1) - 1  # 2^15 - 1 = 32767 output range [-32767,32767]
        wave = amp * wave
        two_ch_wave = np.vstack([wave, wave]).reshape(-1, 2).astype(np.int16)
        sound = pg.sndarray.make_sound(two_ch_wave)
        return sound

    def play(self, effect):
        if effect in self.__effects:
            self.__effects[effect].play()


class Game:
    def __init__(self):
        self.__runner = Runner(20, 220)
        self.__obstacle = Obstacle(700, 260)
        self.__score = 0
        self.__jump = 0
        self.__level = 1
        self.__speed = 5
        self.__state = "starting"
        self.__has_passed_obstacle = False
        self.__drawer = Drawer()
        self.__start_time = None
        self.__save_file = SaveFile()
        self.__data = []

    def reset_game(self):
        """Reset the game."""
        print("Restarting Game...")
        self.__runner = Runner(20, 220)
        self.__obstacle = Obstacle(740, 260)
        self.__score = 0
        self.__level = 1
        self.__speed = 5
        self.__jump = 0
        self.__state = "starting"
        self.__has_passed_obstacle = False
        self.__start_time = None
        self.__data = []

    def find_dis(self):
        """Check if the runner collides with the obstacle."""
        return self.__runner.get_rect().colliderect(self.__obstacle.get_rect())

    def check_is_on_top(self):
        """Check if the runner lands on top of the obstacle."""
        runner_rect = self.__runner.get_rect()
        obs_rect = self.__obstacle.get_rect()

        is_above = obs_rect.top + 20 < runner_rect.bottom
        is_within_x_range = (runner_rect.right > obs_rect.left) and (runner_rect.left < obs_rect.right)

        return is_above and is_within_x_range

    def run(self):
        print("Game loop started")
        running = True
        while running:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
                elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_SPACE:
                        if self.__state == "starting":
                            self.__state = "playing"
                            self.__start_time = time.time()
                            SoundEffects.get_instance().play('start')
                            print("Game started!")
                        elif self.__state == "playing":
                            SoundEffects.get_instance().play('jump')
                            self.__jump += 1
                            self.__runner.jump()
                        elif self.__state == "game over":
                            self.reset_game()

            if self.__state == "starting":
                self.__drawer.drawing_start()
            elif self.__state == "playing":
                self.__runner.update()
                self.__obstacle.update(self.__level, self.__speed)

                if self.find_dis():
                    elapsed_time = time.time() - self.__start_time
                    print(f"Game Over! You survived for {elapsed_time:.2f} seconds.")
                    self.__state = "game over"
                    print("Collision detected! Game Over.")
                    SoundEffects.get_instance().play('over')
                    # self.__data.append(self.__jump)
                    # self.__data.append(self.__score)
                    # self.__data.append(self.__level)
                    # self.__data.append(round(elapsed_time, 2))
                    # self.__data.append(self.__speed)
                    # self.__save_file.add_data(self.__data)

                elif (self.check_is_on_top()
                        or self.__obstacle.get_rect().right < self.__runner.get_rect().left):
                    if not self.__has_passed_obstacle:
                        print("Score increased! Runner either landed or jumped over.")
                        self.__score += 1
                        if self.__score % 10 == 1 and self.__score != 1:
                            self.__level += 1
                            self.__speed += 1
                            self.__has_passed_obstacle = True
                        self.__has_passed_obstacle = True
                else:
                    self.__has_passed_obstacle = False

                self.__drawer.draw_game(self.__runner, self.__obstacle, self.__score, self.__level)
            elif self.__state == "game over":
                self.__drawer.drawing_game_over(self.__score)

            self.__drawer.update()
            self.__drawer.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
