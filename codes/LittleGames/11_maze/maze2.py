from random import choice, randrange
from time import sleep
import turtle as t

# 设置参数
BG_WIDTH, BG_HEIGHT = 660, 660
MY_BG_COLOR = "#181914"
MSG_BG_COLOR = "#1E1E1E"
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

# levels
levels = []
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP         G            X",
    "XXXXXXXXXX     XXXXXXXXXX",
    "XXXXXXXXXX     XXXXXXXXXX",
    "XX                     XX",
    "XX                     XX",
    "XXXXXXXXXX X X XXXXXXXXXX",
    "XXEXXXXXXX X X XXXXXXXXXX",
    "XXXXX      X X      XXXXX",
    "XXX        X X        XXX",
    "XXX    XXXXX XXXX      XX",
    "XX     XXXXX XXXX  E   XX",
    "XX XXXXXXXXX XXXXXXXXX XX",
    "XX                     XX",
    "XX XXXXXXXXX XXXXXXXXX XX",
    "XX                      X",
    "XXXXXXXXXXX   XXXXXXXXXXX",
    "XXXXXXE       XXX XXX   X",
    "X  XXX XX XXX XXX XXX   X",
    "X  XXX XX XXX XXX XXX   X",
    "X  XXX XX XXX XXX XXX   X",
    "X  XXX XX               X",
    "X  XXX XXXXXXXXXXXXXXX  X",
    "X                       X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"]
level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XX         P       G   XX",
    "XX   XXXXXXXXXXXXXXX   XX",
    "XX   XXXXXXXXXXXXXXX   XX",
    "XX                     XX",
    "XX                     XX",
    "XXXXXXXXXX XXX XXXXXXXXXX",
    "XXEXXXXXXX XXX XXXXXXXXXX",
    "XXX        XXX        XXX",
    "XXX        XXX        XXX",
    "XXX    XXXXX XXXX      XX",
    "XX     XXXXX XXXX  E   XX",
    "XX  XXXXXXXX XXXXXXXX  XX",
    "XX                     XX",
    "XX  XXXXXXXX XXXXXXXX  XX",
    "XX                     XX",
    "XXXXXXXXXXX   XXXXXXXXXXX",
    "X     E                 X",
    "X  XXXXXXXXXXXXXXXXXX   X",
    "X                       X",
    "X  XXXXXXXXXXXXXXXXXX   X",
    "X                       X",
    "X  XXXXXXXXXXXXXXXXXX   X",
    "X                       X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"]
levels.append(level_1)
levels.append(level_2)
current_level = 1


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
        if (go_x, go_y) not in walls:
            self.goto(go_x, go_y)
            self.look_for_gold(go_x, go_y)

    def look_for_gold(self, go_x, go_y):
        global score
        for g in golds:
            if g.distance(player) == 0:
                score += 1
                print(score)
                g.hideturtle()
                golds.remove(g)
        if not golds:
            success()


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
class Wall(t.Turtle):
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

    def make_maze(self):
        global cnt_golds
        level = levels[current_level - 1]
        for i, row in enumerate(level):
            screen_y = 288 - 24 * i
            for j, c in enumerate(row):
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
wall = Wall()
wall.make_maze()
success_pen = t.Turtle()


# 下一关
def next_level():
    global current_level, score
    # 更新关卡level
    current_level = current_level % len(levels) + 1
    # 分数清零
    score = 0
    # 清空提示
    success_pen.clear()
    # 隐藏恶魔
    for e in evils:
        e.hideturtle()
    # 清空恶魔
    evils.clear()
    # 清空砖块坐标
    walls.clear()
    # 删除砖块
    wall.clear()

    # 重建迷宫
    wall.make_maze()
    # 给恶魔加上定时器，让它们动起来
    for e in evils:
        t.ontimer(e.move, randrange(100, 300))


# 键盘监听
mz.listen()
mz.onkey(player.go_left, "Left")
mz.onkey(player.go_right, "Right")
mz.onkey(player.go_up, "Up")
mz.onkey(player.go_down, "Down")
mz.onkey(next_level, "Return")

# 给恶魔定闹钟
for e in evils:
    t.ontimer(e.move, randrange(100, 300))  # ?ms 后调用 move()


def show_success_msg(title, msg):
    success_pen.hideturtle()
    success_pen.penup()
    success_pen.speed(0)
    success_pen.fillcolor(MSG_BG_COLOR)
    success_pen.goto(-150, -150)
    success_pen.begin_fill()
    for _ in range(4):
        success_pen.forward(300)
        success_pen.left(90)
    success_pen.end_fill()
    success_pen.goto(0, 0)
    success_pen.color("yellow")
    success_pen.write(title, align="center", font=("Arial", 18, "bold"))
    success_pen.goto(0, -50)
    success_pen.write(msg, align="center", font=("Arial", 16, "bold"))


# 过关
def success():
    if current_level == len(levels):
        show_success_msg("恭喜你，通关了！！！", "重新开始：Enter")
    else:
        show_success_msg("恭喜你，过关了！", "进入下一关：Enter")


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
