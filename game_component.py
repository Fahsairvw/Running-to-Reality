import pygame as pg
from config import Config


class Runner:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__ground_y = y
        self.__velocity = 0
        self.__gravity = 0.4
        self.__is_jumping = False
        self.__runner_images = Config.run
        self.__jump_image = Config.jump
        self.__runner_index = 0
        self.__frame_count = 0

    def update(self):
        """Update runner's animation and jumping logic using projectile motion."""
        self.__frame_count += 1

        if not self.__is_jumping:
            if self.__frame_count % 10 == 0:
                self.__runner_index = (self.__runner_index + 1) % len(self.__runner_images)

        if self.__is_jumping:
            self.__y += self.__velocity
            self.__velocity += self.__gravity

            if self.__y >= self.__ground_y:
                self.__y = self.__ground_y
                self.__is_jumping = False
                self.__velocity = 0

    def draw(self, screen):
        """Draw the runner on the screen."""
        if self.__is_jumping:
            screen.blit(self.__jump_image, (self.__x, self.__y))
        else:
            screen.blit(self.__runner_images[self.__runner_index], (self.__x, self.__y))

    def jump(self):
        """Trigger a projectile-like jump."""
        if not self.__is_jumping:
            self.__is_jumping = True
            self.__velocity = -16

    def get_rect(self):
        """Return the rectangle for collision detection."""
        return pg.Rect(self.__x, self.__y, self.__runner_images[self.__runner_index].get_width(),
                       self.__runner_images[self.__runner_index].get_height())


class Obstacle:
    def __init__(self, x, y):
        self.__obstacle = Config.obstacle
        self.__x = x
        self.__y = y
        self.__reset_flag = False

    def draw(self, screen):
        """Draw the obstacle on the screen."""
        screen.blit(self.__obstacle, (self.__x, self.__y))

    def update(self, level, speed):
        """Update the obstacle's position."""
        self.__x -= (speed + level)
        if self.__x < -self.__obstacle.get_width():
            self.__x = Config.game_width
            self.__reset_flag = True
        else:
            self.__reset_flag = False

    def get_rect(self):
        return pg.Rect(self.__x, self.__y, self.__obstacle.get_width(), self.__obstacle.get_height())


class Drawer:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((Config.game_width, Config.game_height))
        self.__clock = pg.time.Clock()
        self.__bg = Config.bg
        self.__showing = pg.Surface((Config.game_width, Config.game_height), pg.SRCALPHA)

    def draw_game(self, runner, obstacle, score, level):
        """Draw the game screen."""
        self.__screen.blit(self.__bg, (0, 0))
        runner.draw(self.__screen)
        obstacle.draw(self.__screen)

        font = pg.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, Config.black)
        self.__screen.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {level}", True, Config.black)
        self.__screen.blit(level_text, (10, 40))

    def drawing_start(self):
        """Draw the start screen"""
        transparent_surface = pg.Surface((Config.game_width, Config.game_height), pg.SRCALPHA)
        transparent_surface.fill((255, 255, 255, 128))

        font = pg.font.Font(None, 48)
        line1_text = font.render("Escaping F Grade With Me", True, (0, 0, 0))
        line2_text = font.render("Press Space Bar to Begin the journey!", True, (0, 0, 0))

        rect1 = line1_text.get_rect(center=(Config.game_width // 2, (Config.game_height // 2) - 60))
        rect2 = line2_text.get_rect(center=(Config.game_width // 2, Config.game_height // 2))

        transparent_surface.blit(line1_text, rect1)
        transparent_surface.blit(line2_text, rect2)

        self.__screen.blit(transparent_surface, (0, 0))

    def drawing_game_over(self, score):
        """Draw the game over screen"""
        transparent_surface = pg.Surface((Config.game_width, Config.game_height), pg.SRCALPHA)
        transparent_surface.fill((255, 255, 255, 128))

        # Render text
        font = pg.font.Font(None, 48)
        line1_text = font.render(f"Your total score is {score}", True, (0, 0, 0))
        line2_text = font.render("Sorry it not enough to pass the exam", True, (0, 0, 0))
        line3_text = font.render("Press Space bar to restart", True, (0, 0, 0))

        rect1 = line1_text.get_rect(center=(Config.game_width // 2, (Config.game_height // 2) - 60))
        rect2 = line2_text.get_rect(center=(Config.game_width // 2, Config.game_height // 2))
        rect3 = line3_text.get_rect(center=(Config.game_width // 2, (Config.game_height // 2) + 60))

        # Blit text onto the transparent surface
        transparent_surface.blit(line1_text, rect1)
        transparent_surface.blit(line2_text, rect2)
        transparent_surface.blit(line3_text, rect3)

        # Blit the transparent surface onto the screen
        self.__screen.blit(transparent_surface, (0, 0))

    @staticmethod
    def update():
        """Update the display."""
        pg.display.update()

    def tick(self, fps):
        """Control the frame rate."""
        self.__clock.tick(fps)
