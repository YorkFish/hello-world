from random import choice, randrange
from time import sleep
import turtle as t

# 设置参数
BG_WIDTH, BG_HEIGHT = 660, 660
MY_BG_COLOR = "#181914"
running = True

# 创建游戏背景
mz = t.Screen()
mz.setup(BG_WIDTH, BG_HEIGHT)
mz.bgcolor(MY_BG_COLOR)
mz.title("迷宫小游戏")
mz.tracer(0)  # 取消自动刷新

# 注册图片
mz.register_shape("wall.gif")
mz.register_shape("player_left.gif")
mz.register_shape("player_right.gif")
mz.register_shape("gold.gif")
mz.register_shape("ghost.gif")

# level1
levels = []
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP                      X",
    "XXXXXXXXXX  G  XXXXXXXXXX",
    "XXXXXXXXXX     XXXXXXXXXX",
    "XX                     XX",
    "XX                 G   XX",
    "XXXXXXXXXX X X XXXXXXXXXX",
    "XXEXXXXXXX X X XXXXXXXXXX",
    "XXXXX      X X      XXXXX",
    "XXX        X X        XXX",
    "XXX    XXXXX XXXX      XX",
    "XX    GXXXXX XXXX  E   XX",
    "XX XXXXXXXXX XXXXXXXXX XX",
    "XX                     XX",
    "XX XXXXXXXXX XXXXXXXXX XX",
    "XX                      X",
    "XXXXXXXXXXX   XXXXXXXXXXX",
    "XXXXXXE       XXX XXX   X",
    "X  XXX XX XXX XXX XXX   X",
    "X  XXX XX XXX XXX XXX   X",
    "X  XXX XX XXX XXX XXX   X",
    "X  XXX XX   G           X",
    "X  XXX XXXXXXXXXXXXXXX  X",
    "X                       X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"]
levels.append(level_1)


# 创建玩家类
class Player(t.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.shape("player_right.gif")

    def go_left(self):
        go_x = self.xcor() - 24
        go_y = self.ycor()
        self.shape("player_left.gif")
        self.move(go_x, go_y)

    def go_right(self):
        go_x = self.xcor() + 24
        go_y = self.ycor()
        self.shape("player_right.gif")
        self.move(go_x, go_y)

    def go_up(self):
        go_x = self.xcor()
        go_y = self.ycor() + 24
        self.move(go_x, go_y)

    def go_down(self):
        go_x = self.xcor()
        go_y = self.ycor() - 24
        self.move(go_x, go_y)

    def move(self, go_x, go_y):
        # if level_1[(288 - go_y) // 24][(go_x + 288) // 24] != 'X':
        if (go_x, go_y) not in walls:
            self.goto(go_x, go_y)
            self.look_for_gold(go_x, go_y)
        # else:
        #     print("Oh, no! Hitting wall!")

    def look_for_gold(self, go_x, go_y):
        global score
        for g in golds:
            if g.distance(player) == 0:
                score += 1
                print(score)
                g.hideturtle()
                golds.remove(g)


# 创建金币
class Gold(t.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.shape("gold.gif")


# 创建恶魔
class Evil(t.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.shape("ghost.gif")
        self.direction = ' '

    def move(self):
        self.turn()
        go_x = self.xcor()
        go_y = self.ycor()
        if self.direction == 'L':
            go_x -= 24
            if go_x < -288:
                go_x = -288
        elif self.direction == 'R':
            go_x += 24
            if go_x > 288:
                go_x = 288
        elif self.direction == 'U':
            go_y += 24
            if go_y > 288:
                go_y = 288
        elif self.direction == 'D':
            go_y -= 24
            if go_y < -288:
                go_y = -288
        self.goto(go_x, go_y)
        t.ontimer(self.move, randrange(100, 300))  # 给恶魔续钟

    def turn(self):
        # 跟踪功能
        if self.distance(player) < 96:
            if self.xcor() < player.xcor():
                self.direction = 'R'
            elif player.xcor() < self.xcor():
                self.direction = 'L'
            elif self.ycor() < player.ycor():
                self.direction = 'U'
            elif player.ycor() < self.ycor():
                self.direction = 'D'
        else:
            self.direction = choice(['L', 'R', 'U', 'D'])


# 创建墙类
class Pen(t.Turtle):
    """
    wall.gif: 24x24
    maze: 25x25
    25X24/2 - 24/2 = 288
    w, h = -288 + 24 * i, 288 - 24 * i
    """
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.shape("wall.gif")
        self.goto(200, 200)
        self.showturtle()

    def make_maze(self, level):
        for i, row in enumerate(level):  # 25
            screen_y = 288 - 24 * i
            for j, c in enumerate(row):  # 25
                screen_x = -288 + 24 * j
                if c == 'X':  # wall
                    self.goto(screen_x, screen_y)
                    self.stamp()  # 盖章，相当于固定住
                    walls.append((screen_x, screen_y))
                elif c == 'P':  # person
                    player.goto(screen_x, screen_y)
                    player.showturtle()
                elif c == 'G':  # gold
                    gold = Gold()
                    golds.append(gold)
                    gold.goto(screen_x, screen_y)
                    gold.showturtle()
                elif c == 'E':  # evil
                    evil = Evil()
                    evils.append(evil)
                    evil.goto(screen_x, screen_y)
                    evil.showturtle()


walls = []
golds = []
evils = []
score = 0  # number of golds
player = Player()
wall = Pen()
wall.make_maze(levels[0])

# 键盘监听
mz.listen()
mz.onkey(player.go_left, "Left")
mz.onkey(player.go_right, "Right")
mz.onkey(player.go_up, "Up")
mz.onkey(player.go_down, "Down")

# 给恶魔定闹钟
for e in evils:
    t.ontimer(e.move, randrange(100, 300))  # ?ms 后调用 move()


# 判断是否要退出
def stop_loop():
    global running
    running = False


# 获得窗口的 Tk 对象，并注册关闭事件
root = mz.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", stop_loop)

while running:
    mz.update()
    sleep(0.01)

# mz.mainloop()
