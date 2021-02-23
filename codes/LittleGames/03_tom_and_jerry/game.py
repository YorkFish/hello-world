import turtle as t
from random import randint
from time import sleep, time

# 设置参数
BG_WIDTH, BG_HEIGHT = 500, 500
WALL_RIGHT = BG_WIDTH // 2
WALL_LEFT = -WALL_RIGHT
WALL_TOP = BG_HEIGHT // 2
WALL_BOTTOM = -WALL_TOP

RAT_SIZE = 30
RAT_INIT_START = WALL_LEFT + RAT_SIZE // 2
RAT_INIT_STOP = WALL_RIGHT - RAT_SIZE // 2
RAT_OUT = 300
CATCH_DISTANCE = 10
cat_speed = 2
rat_speed = 1

PEN_WIDTH, PEN_HEIGHT = 140, 220
SCORE_WIDTH, SCORE_HEIGHT = 200, 220
GAMEOVER_WIDTH, GAMEOVER_HEIGHT = -180, 0
running = True

# 创建背景
game = t.Screen()
game.setup(BG_WIDTH, BG_HEIGHT)
game.bgpic("tom_bg.png")
t.tracer(3)  # 循环三次，刷新一次

# 加上计时
start_time = time()
used_time = 0

pen = t.Turtle()
pen.hideturtle()
pen.penup()
pen.setposition(PEN_WIDTH, PEN_HEIGHT)
pen.color("red")
pen.write("Time: ", align="left", font=("Arial", 16, "bold"))

pen2 = t.Turtle()
pen2.hideturtle()
pen2.penup()
pen2.setposition(SCORE_WIDTH, SCORE_HEIGHT)
pen2.color("red")


def update_time():
    global start_time
    global used_time
    now_used_time = int(time() - start_time)
    if used_time < now_used_time:
        used_time = now_used_time
        time_str = str(used_time)
        pen2.clear()
        pen2.write(time_str, align="left", font=("Arial", 16, "bold"))


# 创建猫咪
cat = t.Turtle()
cat.penup()
cat.color("yellow")
cat.shapesize(2, 2)
cat.speed(0)

# 创建老鼠
t.register_shape("rat.gif")
rats_number = 10
rats = []
for _ in range(rats_number):
    rat = t.Turtle()
    rats.append(rat)
    rat.hideturtle()
    rat.penup()
    rat.shape("rat.gif")
    rat.speed(0)
    rat.left(randint(1, 360))
    x = randint(RAT_INIT_START, RAT_INIT_STOP)
    y = randint(RAT_INIT_START, RAT_INIT_STOP)
    rat.setposition(x, y)
    rat.showturtle()


def move_left():
    cat.left(30)


def move_right():
    cat.right(30)


def speed_up():
    global cat_speed
    cat_speed += 1


def speed_down():
    global cat_speed
    cat_speed -= 1
    if cat_speed < 0:
        cat_speed = 0


def catch(rat):
    global rats_number
    if cat.distance(rat) < CATCH_DISTANCE:
        rat.hideturtle()
        rat.setpos(RAT_OUT, RAT_OUT)
        rats_number -= 1


t.listen()
t.onkey(move_left, "Left")
t.onkey(move_right, "Right")
t.onkey(speed_up, "Up")
t.onkey(speed_down, "Down")


# 判断是否要退出
def stop_loop():
    global running
    running = False


# 获得窗口的 Tk 对象，并注册关闭事件
root = game.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", stop_loop)

while running:
    update_time()
    cat.forward(cat_speed)
    x = cat.xcor()
    y = cat.ycor()
    if x < WALL_LEFT or WALL_RIGHT < x or y < WALL_BOTTOM or WALL_TOP < y:
        cat.left(180)

    # 让所有的小老鼠都动起来
    for rat in rats:
        if rat.xcor == 300:
            continue
        rat.forward(rat_speed)
        catch(rat)
        x = rat.xcor()
        y = rat.ycor()
        if x < WALL_LEFT or WALL_RIGHT < x or y < WALL_BOTTOM or WALL_TOP < y:
            rat.left(180)

    # 结束
    if rats_number == 0:
        pen3 = t.Turtle()
        pen3.hideturtle()
        pen3.penup()
        pen3.setposition(GAMEOVER_WIDTH, GAMEOVER_HEIGHT)
        pen3.color("red")
        over_str = "Game Over! Used Time: %ds" % used_time
        pen3.write(over_str, align="left", font=("Arial", 20, "bold"))
        break

# game.mainloop()
