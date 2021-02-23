class Person(object):
    def __init__(self, id_num, name):
        self.id = id_num
        self.name = name
        self.records = []  # [Record r1, ...]
        self.scores = {}  # {friend1.id: friend1.score, ...}

    def add_record(self, record):
        self.records.append(record)
        self.scores.setdefault(record.person.id, 0)
        self.scores[record.person.id] += record.score

    def remove_record(self, record):  # 其实这里与实际生活不符
        self.records.remove(record)


class Record(object):
    def __init__(self, person, action, socre):
        self.person = person
        self.action = action
        self.score = socre


# use pytest
def test_record():
    p1 = Person(1, "张三")
    p2 = Person(2, "李四")
    r = Record(p1, "暴打", -5)

    p2.add_record(r)
    assert len(p2.records) == 1, "should have be 1 record"

    p2.remove_record(r)
    assert len(p2.records) == 0, "should have no record"
