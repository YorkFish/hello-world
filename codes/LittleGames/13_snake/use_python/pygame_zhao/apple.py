# coding: utf-8

from random import randrange
from settings import *


class Apple(object):
    """贪吃蛇的食物"""
    def __init__(self, game):
        self.x = 0
        self.y = 0
        self.game = game
        self.game.add_draw_action(self.draw)
        self.drop()

    def drop(self):
        snake = self.game.snake.body + [self.game.snake.head]
        while True:
            x, y = randrange(0, COLS), randrange(0, ROWS)
            if (x, y) not in snake:
                self.x, self.y = x, y
                break

    def draw(self):
        pos = (self.x, self.y)
        self.game.draw_cell(pos, CELL_SIZE, COLOR_APPLE_SKIN, COLOR_APPLE_BODY)
