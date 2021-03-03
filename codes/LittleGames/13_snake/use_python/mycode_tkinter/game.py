import queue
import random
import threading
import time

from tkinter import *


# Parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
CELL_SIZE = 20
COLOR_SNAKE = "#FFCC4C"


class Food(object):
    '''
    功能：
        1. 出现在画面的某个地方
        2. 更改位置
    '''
    def __init__(self):
        '''自动产生一个食物'''
        self.cs = CELL_SIZE
        self.wall_top = self.cs
        self.wall_right = SCREEN_WIDTH
        self.wall_bottom = SCREEN_HEIGHT
        self.wall_left = self.cs
        self.generate_food_pos()  # self.pos

    def generate_food_pos(self):
        '''产生一个食物，即随机产生一个食物的坐标'''
        x = random.randrange(self.wall_left, self.wall_right, self.cs)
        y = random.randrange(self.wall_top, self.wall_bottom, self.cs)
        self.pos = x, y


class Snake(threading.Thread):
    '''
    功能：
        1. 上下左右键控制蛇移动
        2. 每次移动，都需要重新计算蛇头的位置
        3. 检测游戏是否结束
    '''
    def __init__(self, world, queue):
        threading.Thread.__init__(self)

        self.world = world
        self.queue = queue
        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.cs = CELL_SIZE
        self.half_cs = CELL_SIZE // 2
        self.score = 0
        self.body = [(300 - i * self.cs, 60) for i in range(3)]
        self.direction = "Right"
        self.food = Food()
        self.change_food_pos()

        self.start()

    def change_food_pos(self):
        '''防止新的食物出现在蛇身上'''
        while self.food.pos in self.body:
            self.food.generate_food_pos()
        # 消息格式：{消息类型: 此类型的数据}
        x, y = self.food.pos
        self.exppos = x - self.half_cs, y, x + self.half_cs, y
        self.queue.put({"food": self.exppos})

    def key_pressed(self, e):
        '''获取按键'''
        key = e.keysym  # keysym 是按键名
        if (key == "Up" and self.direction in ("Left", "Right")
                or key == "Right" and self.direction in ("Up", "Down")
                or key == "Down" and self.direction in ("Left", "Right")
                or key == "Left" and self.direction in ("Up", "Down")):
            self.direction = key

    def cal_new_pos(self):
        '''计算新的蛇头的位置'''
        x, y = self.body[0]
        if self.direction == "Up":
            y -= self.cs
        elif self.direction == "Right":
            x += self.cs
        elif self.direction == "Down":
            y += self.cs
        elif self.direction == "Left":
            x -= self.cs
        return x, y

    def check_game_over(self, new_head):
        '''
        游戏结束的情况：
            1. 蛇头撞墙
            2. 蛇头撞自己身体
        '''
        x, y = new_head
        if (new_head in self.body
                or x < 0 or self.sw < x
                or y < 0 or self.sh < y):
            self.queue.put({"game_over": True})

    def move(self):
        '''
        1. 重新计算蛇头的坐标
        2. 蛇头与食物相遇后：加分、重新生成食物、通知 world 加分
        3. 保持移动
        '''
        new_head = self.cal_new_pos()
        self.check_game_over(new_head)
        self.body.insert(0, new_head)
        if self.food.pos == new_head:
            self.score += 1
            self.queue.put({"score": self.score})
            self.food.generate_food_pos()
            self.change_food_pos()
        else:
            self.body.pop()

    def run(self):
        '''
        一启用多线程就调用此函数
        要求蛇保持移动
        '''
        if self.world.is_game_over:
            self._delete()
        while not self.world.is_game_over:
            self.queue.put({"move": self.body})
            time.sleep(0.1)  # 控制蛇的速度
            self.move()


class World(Tk):
    '''模拟游戏画板'''
    def __init__(self, queue):
        Tk.__init__(self)

        self.queue = queue
        self.is_game_over = False
        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.cs = CELL_SIZE
        self.canvas = Canvas(self, width=self.sw, height=self.sh, bg="gray")
        self.canvas.pack()
        self.snake = self.canvas.create_line((0, 0), (0, 0),
                                             fill=COLOR_SNAKE, width=self.cs)
        self.food = self.canvas.create_line((0, 0), (0, 0),
                                            fill=COLOR_SNAKE, width=self.cs)
        self.score = self.canvas.create_text(self.sw - 60, 30,
                                             fill="white", text="Score: 0")
        self.queue_handler()

    def queue_handler(self):
        try:
            while True:
                task = self.queue.get(block=False)
                if task.get("game_over"):
                    self.game_over()
                if task.get("move"):
                    # 重新绘制蛇
                    points = [p for pos in task["move"] for p in pos]
                    self.canvas.coords(self.snake, *points)  # 移动 Line
                if task.get("food"):
                    self.canvas.coords(self.food, *task["food"])
                if task.get("score"):
                    text_score = "Score: {}".format(task["score"])
                    self.canvas.itemconfigure(self.score, text=text_score)
                    self.queue.task_done()
        except queue.Empty:  # 抛出队列为空异常
            if not self.is_game_over:
                # after(ms, func) ms 后调用 func
                self.canvas.after(100, self.queue_handler)

    def game_over(self):
        '''游戏结束，清理现场'''
        self.is_game_over = True
        self.canvas.create_text(self.sw // 4, self.sh // 2,
                                fill="white", text="Game Over")
        quit_btn = Button(self, text="Quit", command=self.destroy)
        self.canvas.create_window(self.sw // 4, self.sh // 2 + 20,
                                  anchor="nw", window=quit_btn)


def main():
    q = queue.Queue()

    world = World(q)
    world.title("Snake Game")
    world.geometry("+100+100")

    snake = Snake(world, q)

    world.bind("<Key-Up>", snake.key_pressed)
    world.bind("<Key-Right>", snake.key_pressed)
    world.bind("<Key-Down>", snake.key_pressed)
    world.bind("<Key-Left>", snake.key_pressed)

    world.mainloop()


if __name__ == "__main__":
    main()
