import curses
import random

screen = curses.initscr()
curses.curs_set(0)  # 设置光标为不可见
screen_height, screen_width = screen.getmaxyx()
window = curses.newwin(screen_height, screen_width, 0, 0)
window.keypad(1)  # 某些键生成的转义序列被解释成 curses
window.timeout(100)  # 设置阻塞 100ms，时间一过，返回 -1

snk_y = screen_height // 2
snk_x = screen_width // 4
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

food = [screen_height // 2, screen_width // 2]
window.addch(food[0], food[1], curses.ACS_PI)  # pi 当作食物

key = curses.KEY_RIGHT  # 初始方向

while True:
    next_key = window.getch()
    if next_key != -1:
        key = next_key

    if snake[0][0] in [0, screen_height] or snake[0][1] in [0, screen_width]\
            or snake[0] in snake[1:]:
        curses.endwin()
        quit()

    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1
    snake.insert(0, new_head)

    if snake[0] == food:
        food = None
        while food is None:
            new_food = [
                random.randrange(1, screen_height),
                random.randrange(1, screen_width)
            ]
            if new_food not in snake:
                food = new_food
        window.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)  # 方块当做蛇身
