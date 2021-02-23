## 简单描述

- 可玩性不太高，就是模拟了一些数据，然后通过一些命令查看数据
- 与 `friendbook1` 的不同点
    - 使用了面向对象
    - 有一个生成数据的程序 `generate_data.py`，这样可以不用每次都重新生成数据

## 命令

- `list`: 打印名单
- 输入某人的姓名或ID：打印TA的信息
    - 若有同名同姓的，会列出名单以供选择ID
    - 若输入的名字有效，会打印关系最好的前六位朋友
- `886~`: 退出