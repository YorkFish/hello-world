from data import *


def show_list():
    """
    names: [(1, "张三"), (2, "李四"), ...]
    """
    for idx, name in names:
        print(idx, name)


def show_records(id_num):
    """
    record_dict: {2: [((1, "张三"), "白嫖", (2, "李四"), -1), ...], ...}
    """
    my_records = record_dict.get(id_num, [])
    for record in my_records:
        friend_id, friend_name = record[0]
        action = record[1]
        score = record[3]
        # 张三(1) 给我 点赞 1
        print(f"{friend_name}({friend_id}) 给我 {action} {score}")


def show_summary(id_num):
    """
    name_dict: {1: "张三", ...}
    score_dict
        记录形式：{1: {2: 8, 3: 5, ...}, ...}
        表示意义：{张三: {李四: 8分, 王五: 5分, ...}, ...}
    """
    first_five = list(score_dict[id_num].items())[:5]
    for i, score in first_five:
        print(f"{name_dict[i]}({i}): {score}")


def show_one(idx, name):
    print(f"{idx:0>4}. {name}")
    show_summary(idx)


def find_by_id(id_num):
    """
    names: [(1, "张三"), (2, "李四"), ...]
    """
    idx = int(id_num)
    if 1 <= idx <= 1000:
        show_one(*names[idx - 1])
    else:
        print("输入有误")


def find_by_name(name):
    my_names = [n for n in names if n[1] == name]
    cnt = len(my_names)
    if cnt == 0:
        print(f"没有“{name}”")
    elif cnt == 1:
        show_one(*my_names[0])
    elif cnt > 1:
        for i, n in my_names:
            print(i, n)
        print(f"有{cnt}个“{name}”，请选择对应的id")
