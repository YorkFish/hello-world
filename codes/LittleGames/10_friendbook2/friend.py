from friend_list import show_list, find_by_id, find_by_name

print("""欢迎使用 FriendBook，您可以输入一下命令
list: 显示名单
name: 显示 someone 的信息
886~: 退出""")
while True:
    cmd = input("请输入命令：")
    if cmd == '886~':
        print("再见啦...")
        break
    if cmd == 'list':
        print("名单如下：")
        show_list()
    elif cmd.isdigit():
        find_by_id(cmd)
    else:
        find_by_name(cmd)
