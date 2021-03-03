# coding: utf-8

import pygame
from settings import *


class Snake(object):
    """<======~~~"""
    def __init__(self, game):
        self.sound_eat = pygame.mixer.Sound(SOUND_EAT)
        self.sound_hit = pygame.mixer.Sound(SOUND_HIT)
        self.game = game
        self.game.add_draw_action(self.draw)
        self.reborn()  # head, body, direction, new_direction, speed, alive

    def set_speed(self, speed):
        self._speed = speed
        interval = 1000 / self._speed
        self.game.add_game_action("snake.move", self.move, interval)

    def get_speed(self):
        return self._speed

    speed = property(get_speed, set_speed)

    def draw(self):
        color_skin = COLOR_SNAKE_SKIN if self.alive else COLOR_DEAD_SNAKE_SKIN
        color_body = COLOR_SNAKE_BODY if self.alive else COLOR_DEAD_SNAKE_BODY
        color_head = COLOR_SNAKE_HEAD if self.alive else COLOR_DEAD_SNAKE_HEAD
        for cell in self.body:
            self.game.draw_cell(cell, CELL_SIZE, color_skin, color_body)
        self.game.draw_cell(self.head, CELL_SIZE, color_skin, color_head)

    def turn(self, **kwargs):
        new_dir = kwargs["direction"]
        if (self.direction in [LEFT, RIGHT] and new_dir in [UP, DOWN] or
                self.direction in [UP, DOWN] and new_dir in [LEFT, RIGHT]):
            self.new_direction = new_dir

    def move(self):
        if self.alive:
            # 改变方向
            self.direction = self.new_direction
            # 碰撞检测
            x, y = self.head
            dx, dy = self.direction
            meeting = nx, ny = x + dx, y + dy
            if (meeting in self.body or
                    nx < 0 or COLS <= nx or ny < 0 or ROWS <= ny):
                self.die()
                return
            # 吃到则不断尾巴
            if nx == self.game.apple.x and ny == self.game.apple.y:
                self.sound_eat.play()
                self.game.apple.drop()
                self.game.apple_count += 1
            else:
                self.body.pop()
            # 增加脖子
            self.body.insert(0, self.head)
            # 移动蛇头
            self.head = meeting

    def die(self):
        self.sound_hit.play()
        self.alive = False

    def reborn(self):
        self.head = (SNAKE_INIT_X, SNAKE_INIT_Y)
        self.body = [(-1, -1)] * SNAKE_INIT_BODY_SIZE
        self.direction = SNAKE_INIT_DIRECTION
        self.new_direction = SNAKE_INIT_DIRECTION
        self.speed = SNAKE_INIT_SPEED
        self.alive = True
