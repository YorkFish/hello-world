from level2 import *
from time import time

cycle_count = 0  # 游戏次数
scores = []  # 记录成绩

next_cycle = True
while next_cycle:
    cycle_count += 1
    guess_count = 0
    answer = generate_answer()
    begin_time = time()

    win = False
    while not win:
        guess_count += 1
        guess = make_guess()  # 交卷
        if guess == -1:
            exit()
        result = check_guess(answer, guess)  # 批卷 1A3B
        win = process_result(guess_count, guess, result)  # 结果处理
    used_time = int(time() - begin_time)
    scores.append((cycle_count, guess_count, used_time))

    show_scores(scores)
    next_cycle = should_continue()
