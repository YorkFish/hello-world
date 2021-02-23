import random as r
import simpleaudio as sa
import turtle as t
from time import sleep

# 设置参数
BG_WIDTH, BG_HEIGHT = 900, 600
BG_BOTTOM = -300
BOY_INIT_X, BOY_INIT_Y = 0, -250
BOY_SIZE = 50
WALL_RIGHT = (BG_WIDTH - BOY_SIZE) // 2
WALL_LEFT = -WALL_RIGHT
GIFT_LEFT, GIFT_RIGHT = -420, 420
GIFT_BOTTOM, GIFT_TOP = 0, 260
GIFT_INIT_TOP = 260
BOMB_INIT_TOP = 270
CATCH_DISTANCE = 40
HIT_DISTANCE = 30
PEN_WIDTH, PEN_HEIGHT = -430, 260
game_over = False

# 创建背景
game = t.Screen()  # 窗口默认大小：屏幕 width* 1/2, height * 3/4
game.setup(BG_WIDTH, BG_HEIGHT)
game.bgpic("christmas_bg.png")
game.title("圣诞礼物大冒险")
game.tracer(0)  # 取消 turtle 的默认刷新

# 注册图片
t.register_shape("boy.gif")
t.register_shape("bomb.gif")
t.register_shape("gift1.gif")
t.register_shape("gift2.gif")
t.register_shape("gift3.gif")

# 注册声音
dead = sa.WaveObject.from_wave_file("dead.wav")

# 创建人物
boy = t.Turtle()
boy.hideturtle()
boy.penup()
boy.shape("boy.gif")
boy.speed(0)
boy.goto(BOY_INIT_X, BOY_INIT_Y)
boy.showturtle()

# 让人物动起来
direction = 'L'
boy_speed = 3

# 生命值与分数
life = 3
score = 0
pen = t.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)
pen.goto(PEN_WIDTH, PEN_HEIGHT)
pen.color("red")
score_text = "score: {}, life: {}".format(score, life)
pen.write(score_text, align="left", font=("Arial", 18, "bold"))


def to_left():
    global direction, boy_speed
    if direction == 'L':
        boy_speed += 1
    else:
        direction = 'L'
        boy_speed = 3


def to_right():
    global direction, boy_speed
    if direction == 'R':
        boy_speed += 1
    else:
        direction = 'R'
        boy_speed = 3


# 键盘监听
t.listen()
t.onkey(to_left, "Left")
t.onkey(to_right, "Right")


# 创建物品：传入图形和数量
def build_goods(shape, num):
    goods_list = []
    for _ in range(num):
        g = t.Turtle()
        goods_list.append(g)
        g.hideturtle()
        g.penup()
        g.shape(shape)
        g.speed(0)
        x = r.randint(GIFT_LEFT, GIFT_RIGHT)
        y = r.randint(GIFT_BOTTOM, GIFT_TOP)
        g.goto(x, y)
        g.showturtle()
        g.fall_speed = r.randint(1, 5)
    return goods_list


# 礼物循环下落
def fall_gifts(gifts, add_score):
    global score
    for g in gifts:
        g.sety(g.ycor() - g.fall_speed)
        if g.ycor() < BG_BOTTOM:
            g.sety(GIFT_INIT_TOP)
        elif g.distance(boy) < CATCH_DISTANCE:
            g.sety(GIFT_INIT_TOP)
            score += add_score
            pen.clear()
            score_text = "score: {}, life: {}".format(score, life)
            pen.write(score_text, align="left", font=("Arial", 18, "bold"))


# 炸弹下落
def fall_bombs(bombs_list):
    global life, game_over
    for bomb in bombs_list:
        bomb.sety(bomb.ycor() - bomb.fall_speed)
        if bomb.ycor() < BG_BOTTOM:
            bomb.sety(BOMB_INIT_TOP)
        elif bomb.distance(boy) < HIT_DISTANCE:
            dead.play()
            bomb.sety(BOMB_INIT_TOP)
            life -= 1
            pen.clear()
            score_text = "score: {}, life: {}".format(score, life)
            pen.write(score_text, align="left", font=("Arial", 18, "bold"))
            if life == 0:
                pen2 = t.Turtle()
                pen2.hideturtle()
                pen2.penup()
                pen2.speed(0)
                pen2.goto(0, 0)
                pen2.color("red")
                pen2.write("Game Over!", align="center",
                           font=("Arial", 30, "bold"))
                game_over = True
                break


gift1_list = build_goods("gift1.gif", 6)
gift2_list = build_goods("gift2.gif", 5)
gift3_list = build_goods("gift3.gif", 4)
bombs_list = build_goods("bomb.gif", 5)

while not game_over:
    sleep(0.01)
    game.update()  # 自主刷新界面
    if direction == 'L':
        boy.setx(boy.xcor() - boy_speed)
    elif direction == 'R':
        boy.setx(boy.xcor() + boy_speed)

    if boy.xcor() < WALL_LEFT:
        boy.setx(WALL_LEFT)
        boy_speed = 0
    elif WALL_RIGHT < boy.xcor():
        boy.setx(WALL_RIGHT)
        boy_speed = 0

    # 礼物下落
    fall_gifts(gift1_list, 2)
    fall_gifts(gift2_list, 3)
    fall_gifts(gift3_list, 5)

    fall_bombs(bombs_list)

game.mainloop()
