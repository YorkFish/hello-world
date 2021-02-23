from random import randint


# 产生一个四位数
def generate_answer():
    return randint(1000, 9999)


# 获取用户输入的猜测值
def make_guess():
    while True:
        guess = input("请输入一个四位数[1000,9999]（q退出）：")
        if guess == 'q' or guess == 'Q':
            return -1
        if not guess.isdecimal():
            print("您输入的不是数字，请输入数字！")
            continue

        guess = int(guess)
        if 1000 <= guess <= 9999:
            return guess
        else:
            print("您输入的数字越界了，请输入[1000,9999]！")


def check_guess(answer, guess):
    nums = [0] * 10
    bulls = cows = 0  # bulls->A, cows->B
    for _ in range(4):
        a = answer % 10
        g = guess % 10
        answer //= 10
        guess //= 10
        if a == g:
            bulls += 1
        else:
            if nums[a] < 0:
                cows += 1
            if nums[g] > 0:
                cows += 1
            nums[a] += 1
            nums[g] -= 1
    return f"{bulls}A{cows}B"


# 赢了，返回 True；否则，返回 False
def process_result(guess_count, guess, result):
    print(f"第{guess_count:2}次：猜 {guess}，结果 {result}")
    if result == "4A0B":
        print("Yeah! You win!")
        return True
    return False


def show_scores(scores):
    print("++++++++++战绩++++++++++")
    print("轮次    猜测次数    用时")
    for c, g, u in scores:
        print(f"{c:<8}{g:<12}{u}s")  # str.ljust(10) 文字靠左并补齐空格
    print('-' * 24)


# rparam: True: 继续; False: 结束
def should_continue():
    con = input("继续(y)，结束(n)：")
    if con == 'y' or con == 'Y':
        return True
    else:
        print("退出游戏，再见啦~")
        return False


if __name__ == "__main__":
    assert check_guess_A(1234, 2345) == 0
    assert check_guess_A(1234, 1345) == 1
    assert check_guess_A(1234, 1245) == 2
    assert check_guess_A(1234, 1235) == 3
    assert check_guess_A(1234, 1234) == 4
