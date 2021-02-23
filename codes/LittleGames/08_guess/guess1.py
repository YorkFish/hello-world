from level1 import *
from random import randint
from time import time

guess_limit = input_limit()  # 猜测次数
scores = []  # 战绩
cycle = 0  # 第几轮

while True:
    cycle += 1
    answer = randint(1, 10)
    is_bingo = False
    guess_count = 0
    begin_time = time()

    # 开始一轮游戏
    while guess_count < guess_limit:
        # 输入猜测
        try:
            guess = int(input("我想了一个数字[1,10]，你猜是几？ "))
        except ValueError:
            print("你输入的不是数字，请重输！")
            continue
        # 判断答案
        if guess == answer:
            is_bingo = True
            break
        elif guess < answer:
            print("小了")
        else:
            print("大了")
        guess_count += 1
    # 处理结果
    used_time = time() - begin_time
    scores.append((cycle, is_bingo, used_time))
    deal_result(is_bingo, answer, used_time)  # 对本轮游戏的总结
    show_scores(scores)  # 显示战绩

    quit_game = input("-" * 20 + "\n继续(y)，结束(n)：")
    if quit_game == 'n':
        print("退出游戏~")
        break
