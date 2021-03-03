import pygame
from pygame.locals import *  # 导入常用的函数和常量

from collections import deque
from random import randrange
from time import sleep

# 参数
GAME_NAME = "Snake Game"
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
UP, RIGHT, DOWN, LEFT = "U", "R", "D", "L"

# 颜色
GREY = pygame.Color(150, 150, 150)
RED = pygame.Color(255, 0, 0)
WHITE = pygame.Color(255, 255, 255)
COLOR_BG = pygame.Color(39, 40, 34)
COLOR_FOOD = pygame.Color(223, 255, 0)
COLOR_SNAKE_HEAD = pygame.Color(0, 95, 255)

# 字体
FONT_NAME = "consolas"
FONT_SIZE = 80

# 初始化
pygame.init()
pygame.display.set_caption(GAME_NAME)
window = pygame.display.set_mode(SCREEN_SIZE)
BASICFONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

fps_clock = pygame.time.Clock()  # 控制游戏速度
snake_head = [100, 100]
snake_body = deque(maxlen=800)
snake_body.extend([[80, 100], [60, 100], [40, 100]])
direction = RIGHT
food = [300, 300]
score = 0


def drawSnake():
    pygame.draw.rect(window, COLOR_SNAKE_HEAD,
                     Rect(snake_head[0], snake_head[1], CELL_SIZE, CELL_SIZE))
    for x, y in snake_body:
        pygame.draw.rect(window, WHITE, Rect(x, y, CELL_SIZE, CELL_SIZE))


def drawFood():
    pygame.draw.rect(window, COLOR_FOOD,
                     Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))


def drawScore():
    # 设置分数的显示颜色
    score_surf = BASICFONT.render(str(score), True, GREY)
    # 设置分数的位置
    score_rect = score_surf.get_rect()
    score_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
    # 绑定以上设置到句柄
    window.blit(score_surf, score_rect)


def keyDetection():
    global direction
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in (K_UP, K_w) and direction in (LEFT, RIGHT):
                direction = UP
            elif event.key in (K_RIGHT, K_d) and direction in (UP, DOWN):
                direction = RIGHT
            elif event.key in (K_DOWN, K_s) and direction in (LEFT, RIGHT):
                direction = DOWN
            elif event.key in (K_LEFT, K_a) and direction in (UP, DOWN):
                direction = LEFT


def updateFood():
    while True:
        food[0] = randrange(CELL_SIZE, SCREEN_WIDTH, CELL_SIZE)
        food[1] = randrange(CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE)
        if food not in snake_body:
            break


def moveSnake():
    global direction, score
    keyDetection()
    snake_body.appendleft(snake_head.copy())
    if snake_head == food:
        score += 1
        updateFood()
    else:
        snake_body.pop()

    if direction == UP:
        snake_head[1] -= CELL_SIZE
    elif direction == RIGHT:
        snake_head[0] += CELL_SIZE
    elif direction == DOWN:
        snake_head[1] += CELL_SIZE
    elif direction == LEFT:
        snake_head[0] -= CELL_SIZE


def checkOver():
    if (snake_head in snake_body
            or snake_head[0] < 0 or SCREEN_WIDTH <= snake_head[0]
            or snake_head[1] < 0 or SCREEN_HEIGHT <= snake_head[1]):
        gameover_surf = BASICFONT.render("Game Over!", True, RED)
        gameover_rect = gameover_surf.get_rect()
        gameover_rect.midtop = (SCREEN_WIDTH // 2, 20)
        window.blit(gameover_surf, gameover_rect)
        pygame.display.flip()

        sleep(3)
        pygame.quit()  # 退出游戏
        quit()  # 退出程序


while True:
    moveSnake()
    checkOver()

    window.fill(COLOR_BG)
    drawSnake()
    drawFood()
    drawScore()

    pygame.display.flip()  # 渲染（画出来）
    fps_clock.tick(10)  # 设置帧频
