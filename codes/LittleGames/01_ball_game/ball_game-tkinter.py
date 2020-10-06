#!/usr/bin/env python3
# coding:utf-8
# 有很大提升空间。。。

import tkinter as tk
from tkinter import messagebox
from time import sleep

# 创建小球的类
class Ball(object):
    def __init__(self, canvas, color):
        """
        参数：画布、颜色
        """
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)        # 左上角坐标(x1,y1)，右下角坐标(x2,y2)；填充色
        self.canvas.move(self.id, 245, 100)                             # 将小球移到画布的(245,100)
        self.x = 3                                                      # 初始的水平方向运动的速度
        self.y = -2                                                     # 初始的竖直方向运动的速度
        self.canvas_height = self.canvas.winfo_height()                 # 获取画布当前的高度
        self.canvas_width = self.canvas.winfo_width()                   # 获取画布当前的宽度
        # print(f">>> h = {self.canvas_height}, w = {self.canvas_width}")
        self.hit_bottom = False                                         # 默认小球没有触底

        return None
    
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)                           # 如 self.pos = [253.0, 108.0, 268.0, 123.0] -> [x1, y1, x2, y2]
        # print(">>> ball.pos =", self.pos)

        if self.pos[0] <= 0:                                             # 左侧
            self.x *= -1
        elif self.pos[2] >= self.canvas_width:                           # 右侧
            self.x *= -1

        if self.pos[1] <= 0:                                             # 上侧
            self.y *= -1
        # elif self.pos[3] >= self.canvas_height:                          # 下侧
        #     self.hit_bottom = True
        #     print("你输了!")

        return None
        

# 创建球拍的类
class Paddle(object):
    def __init__(self, canvas, color):
        """
        参数：画布、颜色
        """
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)    # 创上角坐标(x1,y1)，右下角坐标(x2,y2)；填充色
        self.canvas.move(self.id, 200, 300)                             # 将球拍移到画布的(200,300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()                   # 获取画布当前的宽度
        self.canvas.bind_all("<KeyPress-Left>", self.turn_left)         # 把 turn_left() 函数绑定到左方向键上
        self.canvas.bind_all("<KeyPress-Right>", self.turn_right)       # 把 turn_right() 函数班绑定到右方向键上

        return None

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        self.x = 0

        return None

    def turn_left(self, evt):
        self.pos = self.canvas.coords(self.id)                          # 获得球拍的坐标[x1, y1, x2, y2]
        if self.pos[0] > 0:                                             # 球拍左移
            self.x = -10

        return None

    def turn_right(self, evt):
        self.pos = self.canvas.coords(self.id)                          # 获得球拍的坐标[x1, y1, x2, y2]
        if self.pos[2] < self.canvas_width:                             # 球拍右移
            self.x = 10

       # return None


class GameWindow(object):
    def __init__(self):
        self.game_window = tk.Tk()
        self.game_window.title("Ball Game")                             # 加标题
        self.game_window.resizable(0, 0)                                # 水平、竖直方向防拉伸
        self.game_window.wm_attributes("-topmost", 1)                   # 窗口置顶，1 为使能
        self.game_window.geometry("+450+100")                           # 窗口定位

        self.canvas = tk.Canvas(self.game_window, width=500, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()                                              # 布局 canvas
        self.game_window.update()                                       # 初始化

        self.ball = Ball(self.canvas, "red")                            # 生成小球
        self.ball.draw()
        self.paddle = Paddle(self.canvas, "blue")                       # 生成画板
        self.paddle.draw()

        self.runGame()

        return None

    def runGame(self):
        while not self.ball.hit_bottom:
            self.ball.draw()
            self.paddle.draw()
            self.hit()
            # self.game_window.update_idletasks()
            self.game_window.update()
            sleep(0.02)                                                 # 间隔 20ms
        tk.messagebox.showinfo(title="game over", message="see you next time!")

        return None

    def hit(self):
        if self.ball.pos[3] >= 300:
            if self.ball.pos[0] < self.paddle.pos[2] and self.ball.pos[2] > self.paddle.pos[0]:
                self.ball.y *= -1
                # print(">>> ball.y =", self.ball.y)
            else:
                self.ball.hit_bottom = True
                # print(">>> ball.y =", self.ball.y)

        return None

if __name__ == "__main__":
    GameWindow()

