import pygame as pg


class Config:
    GAME_WIDTH = 800
    GAME_HEIGHT = 600

    MENU_WIDTH = 613
    MENU_HEIGHT = 616

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    BG = {1: pg.image.load("photo/bg.png"), 2: pg.image.load("photo/bg3.png"),  3: pg.image.load("photo/bg2.png")}
    RUN = {1: [pg.image.load("photo/run.png"), pg.image.load("photo/run2.png")], 2: [pg.image.load("photo/run.png"), pg.image.load("photo/run2.png")], 3: pg.image.load("photo/ghost.png")}
    OBSTACLE = {1: pg.image.load("photo/obstacle.png"), 2: pg.image.load("photo/obstacle3.png"),
                3: pg.image.load("photo/obstacle2.png")}
    JUMP = {1: pg.image.load("photo/jump.png"), 2: pg.image.load("photo/jump.png"), 3: pg.image.load("photo/ghost.png")}
    MENU_BG = pg.image.load('photo/menu.png')

    TEXT_STARTING = {1: 'Escaping F Grade With Me', 3: 'Escaping trap with me', 2: 'Escaping time with me'}
    TEXT_ENDING = {1: 'Sorry, it not enough to pass the exam!', 2: 'There is no time left!', 3: 'You got trapped!'}

    POSITION_RUNNER = {'Escaping F': (20, 220), 'Escaping T': (20, 260), 'Rescuing G': (20, 220)}
    POSITION_OBSTACLE = {'Escaping F': (700, 260), 'Escaping T': (700, 330), 'Rescuing G': (700, 240)}

    WHITE = (200, 255, 255)
    BLACK = (0, 0, 0)



