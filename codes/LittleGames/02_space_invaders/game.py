import random
import simpleaudio
import time
import turtle

# 引入音乐
laser = simpleaudio.WaveObject.from_wave_file("laser.wav")  # 发射子弹
explosion = simpleaudio.WaveObject.from_wave_file("explosion.wav")  # 敌机摧毁

# 设置背景
BG_WIDTH, BG_HEIGHT = 500, 500
game = turtle.Screen()
game.setup(BG_WIDTH, BG_HEIGHT)
game.title("Space Game")
game.bgpic("space_bg.png")

# 添加元素，设置位置
turtle.addshape("player.gif")
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 30
RIGHT_WALL = (BG_WIDTH - PLAYER_WIDTH) // 2
LEFT_WALL = -RIGHT_WALL

turtle.addshape("inv.gif")
INV_BOTTOM, INV_TOP = 100, 230

PEN_WIDTH, PEN_HEIGHT = -240, 220

PLAYER_STEP = 15
PLAYER_INIT_BOTTOM = -200
BOMB_STEP = 20
BOMB_INIT_BOTTOM = -300
HIT_DISTANCE = 15
BG_TOP = BG_HEIGHT // 2
LINE_OF_DEFENSE = -230

running = True
game_over = False

# 创建玩家
player = turtle.Turtle()
player.hideturtle()
player.penup()
player.shape("player.gif")
player.setposition(0, PLAYER_INIT_BOTTOM)
player.speed(0)
player.showturtle()


def go_left():
    x = player.xcor()
    x -= PLAYER_STEP
    if x < LEFT_WALL:
        x = LEFT_WALL
    player.setx(x)


def go_right():
    x = player.xcor()
    x += PLAYER_STEP
    if RIGHT_WALL < x:
        x = RIGHT_WALL
    player.setx(x)


turtle.listen()
turtle.onkey(go_left, "Left")
turtle.onkey(go_right, "Right")

# 添加子弹
bomb = turtle.Turtle()
bomb.hideturtle()
bomb.penup()
bomb.shape("triangle")
bomb.shapesize(0.5, 0.5)
bomb.color("yellow")
bomb.seth(90)
bomb.speed(0)


# 发射子弹
def fire():
    global is_fired
    if not is_fired:
        is_fired = True
        laser.play()
        bomb.setposition(player.xcor(), player.ycor() + 20)
        bomb.showturtle()


turtle.onkey(fire, "space")  # not Space

# 添加敌人
num = 6
inv_list = []
for _ in range(num):
    inv = turtle.Turtle()
    inv_list.append(inv)
    inv.hideturtle()
    inv.penup()
    inv.shape("inv.gif")
    inv.speed(0)
    x = random.randint(LEFT_WALL, RIGHT_WALL)
    y = random.randint(INV_BOTTOM, INV_TOP)
    inv.setposition(x, y)
    inv.showturtle()

# 让敌人动起来
inv_step = 2
INV_DOWN_STEP = 60
go_back = False

# 添加分数
score = 0
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.speed(0)
pen.setposition(PEN_WIDTH, PEN_HEIGHT)
score_str = "score: %d" % score
pen.write(score_str, align="left", font=("Arial", 16, "normal"))
is_fired = False


# 判断是否要退出
def stop_loop():
    global running
    running = False


# 获得窗口的 Tk 对象，并注册关闭事件
root = game.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", stop_loop)

while running:
    if game_over:
        pen2 = turtle.Turtle()
        pen2.hideturtle()
        pen2.color("red")
        pen2.write("Game Over!", align="center", font=("Arial", 22, "bold"))
        time.sleep(3)
        break

    for inv in inv_list:
        x = inv.xcor()
        x += inv_step
        inv.setx(x)
        if x < LEFT_WALL or RIGHT_WALL < x:
            go_back = True

        if inv.distance(bomb) < HIT_DISTANCE:
            is_fired = False
            explosion.play()
            inv.setposition(0, INV_TOP)
            bomb.hideturtle()
            bomb.setposition(0, BOMB_INIT_BOTTOM)

            pen.clear()
            score += 10
            score_str = "score: %d" % score
            pen.write(score_str, align="left", font=("Arial", 18, "normal"))

        if inv.ycor() < LINE_OF_DEFENSE:
            game_over = True
            break

    if go_back:
        inv_step *= -1
        go_back = False
        for inv in inv_list:
            inv.sety(inv.ycor() - INV_DOWN_STEP)

    if is_fired:
        y = bomb.ycor()
        y += BOMB_STEP
        bomb.sety(y)
        if BG_TOP < y:
            is_fired = False
            bomb.hideturtle()
            bomb.setposition(0, -BOMB_INIT_BOTTOM)

# game.mainloop()
