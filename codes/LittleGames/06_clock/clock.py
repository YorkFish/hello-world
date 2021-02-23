import datetime as dt
import time
import turtle as t

# 设置参数
BG_WIDTH, BG_HEIGHT = 600, 600
CLOCK_RADIUS = 210
CLOCK_INIT_X, CLOCK_INIT_Y = 0, -CLOCK_RADIUS
SCALE = 20
HOUR_HAND = 80
MINUTE_HAND = 120
SECOND_HAND = 160
SLOGAN_X, SLOGAN_Y = 0, 250
MY_FONT = ("Arial", 18, "bold")
running = True

# 创建背景
game = t.Screen()
game.bgcolor("#181914")
game.setup(BG_WIDTH, BG_HEIGHT)
game.tracer(0)  # 不自动更新

# 创建时钟画笔
pen = t.Turtle()
pen.hideturtle()
pen.pensize(3)
pen.speed(0)


def draw_clock(my_title, h, m, s):
    pen.clear()
    # 画圈
    pen.penup()
    pen.seth(0)
    pen.goto(CLOCK_INIT_X, CLOCK_INIT_Y)
    pen.pendown()
    pen.color("#eeeeee")
    pen.circle(CLOCK_RADIUS)

    # 画刻度
    pen.penup()
    pen.goto(0, 0)
    pen.seth(90)  # 向上
    for _ in range(12):
        pen.forward(190)  # radius - scale
        pen.pendown()
        pen.forward(SCALE)
        pen.penup()
        pen.goto(0, 0)
        pen.right(30)  # 360 / 12
    pen.pensize(2)
    for _ in range(60):
        pen.forward(200)
        pen.pendown()
        pen.forward(10)
        pen.penup()
        pen.goto(0, 0)
        pen.right(6)  # 360 / 60
    pen.pensize(3)

    # 画时针
    pen.penup()
    pen.goto(0, 0)
    pen.color("white")
    pen.seth(90)
    pen.right(h * 30)  # (h + m / 60) / 12 * 360
    pen.pendown()
    pen.forward(HOUR_HAND)

    # 画分针
    pen.penup()
    pen.goto(0, 0)
    pen.color("blue")
    pen.seth(90)
    pen.right(m * 6)  # (m + s / 60) / 60 * 360
    pen.pendown()
    pen.forward(MINUTE_HAND)

    # 画秒针
    pen.penup()
    pen.goto(0, 0)
    pen.color("red")
    pen.seth(90)
    pen.right(s * 6)
    pen.pendown()
    pen.forward(SECOND_HAND)

    # 写标语
    pen.penup()
    pen.goto(SLOGAN_X, SLOGAN_Y)
    pen.color("yellow")
    pen.write(my_title, align="center", font=MY_FONT)


# 判断是否要推出
def stop_loop():
    global running
    running = False


# 获得窗口的 Tk 对象，并注册关闭事件
root = game.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", stop_loop)

while running:
    game.update()  # 自己更新
    now_time = dt.datetime.now()
    my_title = f"Today is {now_time.year}-{now_time.month}-{now_time.day}"
    draw_clock(my_title, now_time.hour, now_time.minute, now_time.second)
    time.sleep(1)

# game.mainloop()
