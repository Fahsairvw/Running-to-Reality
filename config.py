import pygame as pg


class Config:
    game_width = 800
    game_height = 600

    menu_width = 613
    menu_height = 616

    bg = pg.image.load("photo/bg.png")
    run = [pg.image.load("photo/run.png"), pg.image.load("photo/run2.png")]
    obstacle = pg.image.load("photo/obstacle.png")
    jump = pg.image.load("photo/jump.png")
    menu_bg = pg.image.load('photo/menu.png')
    white = (200, 255, 255)
    black = (0, 0, 0)

