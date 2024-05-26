import pygame as pg
import constants as c
from enemies.enemy import EnemyFactory
from world import World
from random import choice


class Game:
    def __init__(self):
        self.width = c.SCREEN_WIDTH
        self.height = c.SCREEN_HEIGTH
        self.win = pg.display.set_mode((self.width, self.height))
        self.enemyes = []
        self.towers = []
        self.lives = 10
        self.money = 100

    def run(self):
        run = True

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

        pg.quit()