# coding: utf-8

from apple import Apple
from mygame import MyGame
from snake import Snake

from settings import *


class PySnake(MyGame):
    """贪吃蛇游戏"""
    def __init__(self):
        super(PySnake, self).__init__(GAME_NAME, ICON,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      DISPLAY_MODE, LOOP_SPEED,
                                      FONT_NAME, FONT_SIZE)
        self.draw_background_line()
        self.snake = Snake(self)
        self.apple = Apple(self)
        self.apple_count = 0
        # 绑定按键
        self.add_key_binding(KEY_UP, self.snake.turn, direction=UP)
        self.add_key_binding(KEY_DOWN, self.snake.turn, direction=DOWN)
        self.add_key_binding(KEY_LEFT, self.snake.turn, direction=LEFT)
        self.add_key_binding(KEY_RIGHT, self.snake.turn, direction=RIGHT)
        self.add_key_binding(KEY_REBORN, self.restart)
        self.add_key_binding(KEY_EXIT, self.game_quit)
        self.add_draw_action(self.show_score)

    def draw_background_line(self):
        self.background.fill(COLOR_BG)
        for col in range(CELL_SIZE, SCREEN_WIDTH, CELL_SIZE):
            self.draw.line(self.background, COLOR_GRID,
                           (col, 0), (col, SCREEN_HEIGHT))
        for row in range(CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE):
            self.draw.line(self.background, COLOR_GRID,
                           (0, row), (SCREEN_WIDTH, row))

    def show_score(self):
        text = "Apple %d" % self.apple_count
        self.draw_text(text, (0, 0), COLOR_SCORE)

        if not self.snake.alive:
            self.draw_text(" GAME OVER ",
                           (SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 - 40),
                           COLOR_DEFEAT, WHITE)
            self.draw_text(" PRESS R TO RESTART ",
                           (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2),
                           GREY, LIGHT_GREY)

        if not self.running and self.snake.alive:
            self.draw_text(" GAME PAUSED ",
                           (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20),
                           LIGHT_GREY, DARK_GREY)

    def restart(self):
        if not self.snake.alive:
            self.apple_count = 0
            self.apple.drop()
            self.snake.reborn()
            self.running = True


if __name__ == "__main__":
    PySnake().run()
