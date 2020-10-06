#!/usr/bin/env python3
# coding:utf-8
# 小游戏说明
#     1. 鼠标控制底部的板子
#     2. 每成功接到球 3 次，球都会在原有速度上加速

import pygame as pg
import random
import time
import sys

pg.init()

game_window = pg.display.set_mode((600, 500))
pg.display.set_caption("Ball Game")
game_font = pg.font.Font(None, 70)  # 默认字体，大小

score = 0
point = 1
count = 0
window_bd = (0, 0, 255)             # blue
font_color = (255, 255, 255)        # white
circle_color = (255, 165, 0)        # yellow
paddle_color = (255, 0, 0)          # red
circle_x = random.randint(20, 580)
circle_y = 20
circle_r = 20
velocity_x = 1
velocity_y = 1

while True:
    game_window.fill(window_bd)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    mouse_x, mouse_y = pg.mouse.get_pos()
    pg.draw.circle(game_window, circle_color, (circle_x, circle_y), circle_r)
    if mouse_x > 500:
        mouse_x = 500
    pg.draw.rect(game_window, paddle_color, (mouse_x, 490, 100, 10))    # y=490, width=100, height=10
    my_text = game_font.render(str(score), False, font_color)
    game_window.blit(my_text, (500, 30))                                # 位置
    circle_x += velocity_x
    circle_y += velocity_y
    if circle_x <= 20 or circle_x >= 580:
        velocity_x *= -1
    if circle_y <= 20:
        velocity_y *= -1
    elif mouse_x-20 < circle_x < mouse_x+120 and 470 <= circle_y <= 500:
        velocity_y *= -1
        score += point
        count += 1
        if count == 3:
            count = 0
            point *= 2
            if velocity_x > 0:
                velocity_x += 1
            else:
                velocity_x -= 1
            velocity_y -= 1
    elif circle_y >= 480 and (circle_x <= mouse_x-20 or circle_x >= mouse_x+120):
        break

    pg.display.update()
    time.sleep(0.005)

