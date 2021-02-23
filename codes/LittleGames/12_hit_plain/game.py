import pygame
from math import sqrt
from random import randrange

# 设置参数
SCREEN_SIZE = BG_WIDTH, BG_HEIGHT = 800, 600
WALL_LEFT, WALL_RIGHT = 0, 736  # 800-64
WALL_BOTTOM = 536  # 600-64
CNT_ENEMY = 6
WHITE = (255, 255, 255)
RED = (255, 0, 0)

is_over = False
running = True
bullets = []  # 保存屏幕内的子弹
enemies = []
player_x, player_y = 368, 500  # x: 800/2 - 64/2
speed_player = 0
score = 0

# 初始化界面
pygame.init()
pygame.display.set_caption("飞机游戏")
screen = pygame.display.set_mode(SCREEN_SIZE)

# 载入图片
# turtle 用中心点算，pygame 用左上角算
bgImg = pygame.image.load("bg.png")  # 32x32
enemyImg = pygame.image.load("enemy.png")  # 64x64
bulletImg = pygame.image.load("bullet.png")  # 32x32
playerImg = pygame.image.load("player.png")  # 64x64

# 添加音效
pygame.mixer.music.load("bg.mp3")  # 背景音乐
# pygame.mixer.music.set_volume()  # 调节音量 0.1-1
pygame.mixer.music.play(-1)  # 单曲循环
bomb = pygame.mixer.Sound("exp.wav")  # 爆炸音效

# 添加字体
font_score = pygame.font.SysFont("simsunnsimsun", 40)  # 宋体
font_over = pygame.font.Font("freesansbold.ttf", 64)  # 创建一个字体


class Enemy(object):
    def __init__(self):
        self.img = enemyImg
        self.x = randrange(200, 600)
        self.y = randrange(50, 250)
        self.step = randrange(2, 6)

    def reset(self):
        self.x = randrange(100, 700)
        self.y = randrange(0, 100)


class Bullet(object):
    def __init__(self):
        self.img = bulletImg
        self.x = player_x + 16  # |16| 32 |16|
        self.y = player_y
        self.step = 10  # 子弹移速

    def _distance(self, enemy):
        dx, dy = self.x - enemy.x, self.y - enemy.y
        return sqrt(dx * dx + dy * dy)

    def hit(self):
        global score
        for e in enemies:
            if self._distance(e) < 30:
                bomb.play()
                if self in bullets:  # 以防万一
                    bullets.remove(self)
                e.reset()
                score += 1
                print(score)


# 生成敌人
for _ in range(CNT_ENEMY):
    enemies.append(Enemy())


def move_enemys():
    global is_over
    for e in enemies:
        e.x += e.step
        # 防止敌机出界
        if e.x < WALL_LEFT or WALL_RIGHT < e.x:
            e.step *= -1
            e.y += 40
        if WALL_BOTTOM < e.y:
            is_over = True
            print("Game Over!")
            break
        screen.blit(e.img, (e.x, e.y))
    if is_over:
        enemies.clear()


def move_player():
    global player_x, player_y, speed_player
    player_x += speed_player
    if player_x < WALL_LEFT:
        player_x = WALL_LEFT
    if WALL_RIGHT < player_x:
        player_x = WALL_RIGHT
    screen.blit(playerImg, (player_x, player_y))


def move_bullets():
    for b in bullets:
        screen.blit(b.img, (b.x, b.y))
        b.hit()
        b.y -= b.step
        if b.y < 0:
            if b in bullets:
                bullets.remove(b)


def show_score():
    text = f"分数：{score}"
    score_render = font_score.render(text, True, WHITE)  # render: 渲染
    screen.blit(score_render, (10, 10))


def check_over():
    if is_over:
        text = "Game Over!"
        render = font_over.render(text, True, RED)
        screen.blit(render, (220, 250))


while running:
    screen.blit(bgImg, (0, 0))
    show_score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        # 按下移动，抬起不动
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_player = -5
            elif event.key == pygame.K_RIGHT:
                speed_player = 5
            elif event.key == pygame.K_SPACE:
                bullets.append(Bullet())
        if event.type == pygame.KEYUP:
            speed_player = 0

    move_player()
    move_bullets()
    move_enemys()
    check_over()

    pygame.display.update()
