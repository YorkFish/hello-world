# coding: utf-8

import os
import pygame
import sys

from settings import *


class MyGame(object):
    """Pygame 模板类"""
    def __init__(self, game_name="My Game", icon=None,
                 screen_width=640, screen_height=480,
                 display_mode=DISPLAY_MODE, loop_speed=60,
                 font_name=FONT_NAME, font_size=16):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(game_name)
        self.icon = icon
        self.icon and pygame.display.set_icon(pygame.image.load(icon))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_size = (screen_width, screen_height)
        self.display_mode = display_mode
        self.screen = pygame.display.set_mode(self.screen_size, display_mode)
        self.loop_speed = loop_speed
        self.font = pygame.font.Font(font_name, font_size)

        self.clock = pygame.time.Clock()
        self.now = 0
        self.running = True
        self.background = pygame.Surface(self.screen_size)

        self.key_bindings = {}  # key: (action, args)
        self.add_key_binding(KEY_PAUSE, self.pause)
        self.game_actions = {}  # action: args
        self.draw_actions = [self.draw_background]
        self.draw = pygame.draw

    def draw_background(self):
        # 图片的左上角与 (0, 0) 对齐
        self.screen.blit(self.background, (0, 0))

    def draw_cell(self, cell, size, color_out, color_in=None):
        x, y = cell
        rect = pygame.Rect(x * size, y * size, size, size)
        self.screen.fill(color_out, rect)
        if color_in:
            self.screen.fill(color_in, rect.inflate(-4, -4))

    def draw_text(self, text, pos, color, bgcolor=None):
        surface = self.font.render(text, True, color, bgcolor)
        self.screen.blit(surface, pos)

    def add_key_binding(self, key, action, **kwargs):
        self.key_bindings[key] = action, kwargs

    def add_game_action(self, name, action, interval=0):
        """添加游戏数据更新动作"""
        next_time = (self.now + interval) if interval else None
        actions = dict(run=action, interval=interval, next_time=next_time)
        self.game_actions[name] = actions

    def add_draw_action(self, action):
        self.draw_actions.append(action)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_bindings:
                    action, kwargs = self.key_bindings[event.key]
                    if kwargs:
                        action(**kwargs)
                    elif action:
                        action()

    def update_gamedata(self):
        for action in self.game_actions.values():
            if not action["next_time"]:
                action["run"]()
            elif action["next_time"] <= self.now:
                action["next_time"] += action["interval"]
                action["run"]()

    def update_display(self):
        for action in self.draw_actions:
            action()  # 依次画部件
        pygame.display.flip()  # 更新画面

    def run(self):
        while True:
            self.now = pygame.time.get_ticks()
            self.process_events()
            if self.running:
                self.update_gamedata()
            self.update_display()
            self.clock.tick(self.loop_speed)

    def pause(self):
        self.running = not self.running
        if self.running:
            for action in self.game_actions.values():
                if action["next_time"]:
                    action["next_time"] = self.now + action["interval"]

    def game_quit(self):
        pygame.quit()
        sys.exit(0)
