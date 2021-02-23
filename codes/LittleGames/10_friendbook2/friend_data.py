from person import *

persons = []


def load_names():
    """
    names.txt
        1 张三
        2 李四
        ...
    """
    with open("names.txt", encoding="utf-8") as f:
        for line in f:
            idx, name = line.split()
            persons.append(Person(int(idx), name))


def load_records():
    """
    recores.txt
        (1, '张三'), '点赞', (2, '李四'), 1
        ...
    """
    with open("records.txt", encoding="utf-8") as f:
        for line in f:
            t1, action, t2, score = eval(line)
            p1 = find_person_by_id(t1[0])
            p2 = find_person_by_id(t2[0])
            if p1 is None or p2 is None:
                continue
            r = Record(p1, action, score)
            p2.add_record(r)


def find_person_by_id(idx):
    for p in persons:
        if p.id == idx:
            return p


def load_data():
    load_names()
    load_records()


load_data()


if __name__ == "__main__":
    for p in persons[:10]:
        print(f"{p.name} has {len(p.records):>3} records.")
