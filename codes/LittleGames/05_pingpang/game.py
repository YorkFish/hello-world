import turtle as t

# 设置参数
BG_WIDTH, BG_HEIGHT = 800, 600
STRETCH_W, STRETCH_L = 5, 1  # 1:20pixel
RACKET_TOP = (BG_HEIGHT - STRETCH_W * 20) // 2
RACKET_BOTTOM = -RACKET_TOP
RACKET_SPEED = 10
BALL_RADIUS = 10
BALL_TOP = BG_HEIGHT // 2 - BALL_RADIUS
BALL_BOTTOM = -BALL_TOP
SCORE_X, SCORE_Y = 0, 260

running = True
score_qiang = 0
score_zhen = 0

# 创建背景
#      ^y
#      |     x
# -----0----->
#      |
game = t.Screen()
game.title("左右互博")
game.setup(BG_WIDTH, BG_HEIGHT)
game.bgcolor("#181914")


# 创建球拍
def build_racket(color, shape, stretch_w, stretch_l, init_x, init_y):
    racket = t.Turtle()
    racket.hideturtle()
    racket.penup()
    racket.color(color)
    racket.shape(shape)
    racket.shapesize(stretch_w, stretch_l)  # 上下拉伸，左右拉伸
    racket.goto(init_x, init_y)
    racket.speed(0)
    racket.showturtle()
    return racket


qiang = build_racket("yellow", "square", STRETCH_W, STRETCH_L, -350, 0)
zhen = build_racket("white", "square", STRETCH_W, STRETCH_L, 350, 0)


def qiang_up():
    y = qiang.ycor()
    y += RACKET_SPEED
    if RACKET_TOP < y:
        y = RACKET_TOP
    qiang.sety(y)


def qiang_down():
    y = qiang.ycor()
    y -= RACKET_SPEED
    if y < RACKET_BOTTOM:
        y = RACKET_BOTTOM
    qiang.sety(y)


def zhen_up():
    y = zhen.ycor()
    y += RACKET_SPEED
    if RACKET_TOP < y:
        y = RACKET_TOP
    zhen.sety(y)


def zhen_down():
    y = zhen.ycor()
    y -= RACKET_SPEED
    if y < RACKET_BOTTOM:
        y = RACKET_BOTTOM
    zhen.sety(y)


game.listen()
game.onkey(qiang_up, 'w')
game.onkey(qiang_down, 's')
game.onkey(zhen_up, 'Up')
game.onkey(zhen_down, 'Down')

# 创建乒乓球
ball = t.Turtle()
ball.penup()
ball.speed(0)
ball.color("orange")
ball.shape("circle")  # 默认半径：10
ball.dx = 2
ball.dy = 2


def write_score():
    pen.clear()
    score_text = "阿强：{}    阿珍：{}".format(score_qiang, score_zhen)
    pen.write(score_text, align="center", font=("Arial", 16, "bold"))


# 设置左上角的分数
pen = t.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(SCORE_X, SCORE_Y)
write_score()


# 判断是否要退出
def stop_loop():
    global running
    running = False


# 获得窗口的 Tk 对象，并注册关闭事件
root = game.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", stop_loop)

while running:
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # 撞上下边界
    if ball.ycor() < BALL_BOTTOM or BALL_TOP < ball.ycor():
        ball.dy *= -1

    # 阿强接球
    # 球拍长 100，宽 20，球直径 20
    qiang_y_up = qiang.ycor() + 50
    qiang_y_down = qiang.ycor() - 50
    # -350 + 20/2 + 20/2 = -330
    if qiang_y_down < ball.ycor() < qiang_y_up and ball.xcor() < -330:
        ball.setx(-328)
        ball.dx *= -1

    # 阿珍接球
    zhen_y_up = zhen.ycor() + 50
    zhen_y_down = zhen.ycor() - 50
    if zhen_y_down < ball.ycor() < zhen_y_up and ball.xcor() > 330:
        ball.setx(328)
        ball.dx *= -1

    # 撞左右边界
    if ball.xcor() <= -380:  # -400 + 20/2 + 20/2
        ball.goto(0, 0)
        score_zhen += 1
        ball.dx *= -1
        write_score()
    elif ball.xcor() >= 380:
        ball.goto(0, 0)
        score_qiang += 1
        ball.dx *= -1
        write_score()

# game.mainloop()
