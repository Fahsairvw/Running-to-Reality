import pygame as pg
from config import Config


class Runner:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__ground_y = y
        self.__velocity = 0
        self.__runner_images = None
        self.__jump_image = None
        self.__is_jumping = False
        self.__runner_index = 0
        self.__frame_count = 0
        self.__theme = None

    def set_theme(self, theme):
        """ set the selected theme"""
        self.__theme = theme
        self.__runner_images = Config.RUN[self.__theme]
        self.__jump_image = Config.JUMP[self.__theme]

    def update(self, gravity):
        """Update runner's animation and jumping logic using projectile motion."""
        if isinstance(self.__runner_images, list):
            self.__frame_count += 1

            if not self.__is_jumping:
                if self.__frame_count % 10 == 0:
                    self.__runner_index = (self.__runner_index + 1) % len(self.__runner_images)

        if self.__is_jumping:
            self.__y += self.__velocity
            self.__velocity += gravity

            if self.__y >= self.__ground_y:
                self.__y = self.__ground_y
                self.__is_jumping = False
                self.__velocity = 0

    def draw(self, screen):
        """Draw the runner on the screen."""
        if self.__is_jumping:
            screen.blit(self.__jump_image, (self.__x, self.__y))
        else:
            if isinstance(self.__runner_images, list):
                screen.blit(self.__runner_images[self.__runner_index], (self.__x, self.__y))
            else:
                screen.blit(self.__runner_images, (self.__x, self.__y))

    def jump(self):
        """Trigger a projectile-like jump."""
        if not self.__is_jumping:
            self.__is_jumping = True
            self.__velocity = -16

    def get_rect(self):
        """Return the rectangle for collision detection."""
        if isinstance(self.__runner_images, list):
            return pg.Rect(self.__x, self.__y, self.__runner_images[self.__runner_index].get_width(),
                           self.__runner_images[self.__runner_index].get_height())
        return pg.Rect(self.__x, self.__y, self.__runner_images.get_width(),
                       self.__runner_images.get_height())


class Obstacle:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__obstacle = None
        self.__reset_flag = False
        self.__theme = None

    def set_theme(self, theme):
        """set the selected theme"""
        self.__theme = theme
        self.__obstacle = Config.OBSTACLE[self.__theme]

    def draw(self, screen):
        """Draw the obstacle on the screen."""
        screen.blit(self.__obstacle, (self.__x, self.__y))

    def update(self, level, speed):
        """Update the obstacle's position."""
        self.__x -= (speed + level)
        if self.__x < - self.__obstacle.get_width():
            self.__x = Config.GAME_WIDTH
            self.__reset_flag = True
        else:
            self.__reset_flag = False

    def get_rect(self):
        """Return the obstacle's position."""
        return pg.Rect(self.__x, self.__y, self.__obstacle.get_width(), self.__obstacle.get_height())


class Drawer:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((Config.GAME_WIDTH, Config.GAME_HEIGHT))
        self.__bg = None
        self.__clock = pg.time.Clock()
        self.__showing = pg.Surface((Config.GAME_WIDTH, Config.GAME_HEIGHT), pg.SRCALPHA)
        self.__theme = None

    def set_theme(self, theme):
        """set the selected theme"""
        self.__theme = theme
        self.__bg = Config.BG[self.__theme]

    def draw_game(self, runner, obstacle, score, level):
        """Draw the game screen."""

        self.__screen.blit(self.__bg, (0, 0))
        runner.draw(self.__screen)
        obstacle.draw(self.__screen)

        font = pg.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, Config.BLACK)
        self.__screen.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {level}", True, Config.BLACK)
        self.__screen.blit(level_text, (10, 40))

    def drawing_start(self):
        """Draw the start screen"""
        self.__screen.fill(Config.WHITE)

        font = pg.font.Font(None, 48)
        line1_text = font.render(Config.TEXT_STARTING[self.__theme], True, (0, 0, 0))
        line2_text = font.render("Press Space Bar to Begin the journey!", True, (0, 0, 0))

        rect1 = line1_text.get_rect(center=(Config.GAME_WIDTH // 2, (Config.GAME_HEIGHT // 2) - 60))
        rect2 = line2_text.get_rect(center=(Config.GAME_WIDTH // 2, Config.GAME_HEIGHT // 2))

        self.__screen.blit(line1_text, rect1)
        self.__screen.blit(line2_text, rect2)

    def drawing_game_over(self, score):
        """Draw the game over screen"""
        transparent_surface = pg.Surface((Config.GAME_WIDTH, Config.GAME_HEIGHT), pg.SRCALPHA)
        transparent_surface.fill((255, 255, 255, 128))

        font = pg.font.Font(None, 48)
        line1_text = font.render(f"Your total score is {score}", True, (0, 0, 0))
        line2_text = font.render(f"{Config.TEXT_ENDING[self.__theme]}", True, (0, 0, 0))
        line3_text = font.render("Press Space bar to restart", True, (0, 0, 0))

        rect1 = line1_text.get_rect(center=(Config.GAME_WIDTH // 2, (Config.GAME_HEIGHT // 2) - 60))
        rect2 = line2_text.get_rect(center=(Config.GAME_WIDTH // 2, Config.GAME_HEIGHT // 2))
        rect3 = line3_text.get_rect(center=(Config.GAME_WIDTH // 2, (Config.GAME_HEIGHT // 2) + 60))

        transparent_surface.blit(line1_text, rect1)
        transparent_surface.blit(line2_text, rect2)
        transparent_surface.blit(line3_text, rect3)

        self.__screen.blit(transparent_surface, (0, 0))

    def updating(self):
        self.__screen = pg.display.set_mode((Config.GAME_WIDTH, Config.GAME_HEIGHT))

    @staticmethod
    def update():
        """Update the display."""
        pg.display.update()

    def tick(self, fps):
        """Control the frame rate."""
        self.__clock.tick(fps)


class Menu:
    def __init__(self):
        self.__screen = pg.display.set_mode((Config.MENU_WIDTH, Config.MENU_HEIGHT))
        self.__menu = Config.MENU_BG
        self.__buttons = {
            "Escaping F": pg.Rect(140, 320, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT),
            "Escaping T": pg.Rect(140, 427, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT),
            "Rescuing G": pg.Rect(140, 528, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT),
        }

        self.selected_theme = None

    def handle_events(self, event):
        """Detect button clicks and update theme selection."""
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            for theme, rect in self.__buttons.items():
                if rect.collidepoint(mouse_pos):
                    self.selected_theme = theme

    def draw_menu(self):
        """draw the menu and button"""
        self.__screen.blit(self.__menu, (0, 0))
        font = pg.font.Font(None, 46)

        for theme, rect in self.__buttons.items():
            pg.draw.rect(self.__screen, Config.WHITE, rect)
            text = font.render(theme, True, Config.BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.__screen.blit(text, text_rect)
