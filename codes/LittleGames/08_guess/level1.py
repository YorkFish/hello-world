import sys


def input_limit():
    try:
        limit = int(sys.argv[1])
    except (IndexError, ValueError):
        limit = 4
        print("输入有误，现在使用默认值：4")
    return limit


def deal_result(is_bingo, answer, used_time):
    if is_bingo:
        print("你猜对了！")
    else:
        print("答案是 %d，再来一次吧！" % answer)
    print("本次猜测共用时 %.2f 秒" % used_time)


def show_scores(scores):
    star = min(scores, key=lambda x: x[2] if x[1] else 60)[0]
    print("++++++++++你的战绩++++++++++")
    print("次数    猜中与否    所用时间")
    for cycle, is_bingo, used_time in scores:
        if star == cycle and is_bingo:
            print(f"*{cycle:<7}{str(is_bingo):<12}{used_time:<.2f}s")
        else:
            print(f"{cycle:<8}{str(is_bingo):<12}{used_time:<.2f}s")
