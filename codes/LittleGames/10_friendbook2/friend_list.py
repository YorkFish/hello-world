from friend_data import *


def show_list():
    for p in persons:
        print(p.id, p.name)


def show_records(person):
    """
    person.id
    person.name
    person.records: [Record r1, Record r2, ...]
    r1: person, action, score
    """
    for r in person.records:
        friend_name, friend_id = r.person.name, r.person.id
        print(f"{friend_name}({friend_id}) 给我 {r.action} | {r.score}")


def show_summary(person):
    great_six = sorted(person.scores.items(), key=lambda x: -x[1])[:6]
    for idx, score in great_six:
        print(persons[idx - 1].name, idx, score)


def show_one(person):
    """
    @param person: (1, "张三")
    """
    print(person.id, person.name)
    show_summary(person)


def find_by_id(id_num):
    idx = int(id_num) - 1
    if 0 <= idx < 100:
        show_one(persons[idx])
    else:
        print("输入有误")


def find_by_name(name):
    names = [p for p in persons if p.name == name]
    cnt = len(names)
    if cnt == 0:
        print(f"没有“{name}”")
    elif cnt == 1:
        show_one(names[0])
    else:
        for p in names:
            print(p.id, p.name)
        print(f"有{cnt}个“{name}”，请选择对应的 id")
