# coding: utf-8
"""
author: York
date: 2021-09-26
"""

import os

from api.PublicApi import *
from applogger import logger
from models.UserinfoModel import Userinfo, UserinfoDAO
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from pages.ReaderinfoPage import ReaderinfoPage
from pages.ReaderListPage import ReaderListPage
from pages.RegisterPage import RegisterPage
from pages.UserinfoPage import UserinfoPage
from pages.WelcomePage import WelcomePage


def user_login(page):
    LoginPage().show()


def user_register(page):
    RegisterPage().show()


def do_register(page):
    """
    @param: page: 当前页面，类似 self
    """
    username = get_input(message="请输入用户名（3-16位）：",
                         check_re=r"^\w{3,16}$")
    logger.debug(f"用户名：{username}")

    nickname = get_input(message="请输入昵称（1-10位）：",
                         check_re=r"^\S{1,10}$")
    logger.debug(f"昵称：{nickname}")

    f_password = get_input(message="请输入密码（6-12位）：",
                           check_re=r"^\w{6,12}$", is_password=True)
    a_password = get_input(message="请确认密码：",
                           warning="两次输入的密码不一致，请重新输入",
                           check_re=f"^{f_password}$", is_password=True)
    logger.debug(f"密码：{a_password}")

    phone = get_input(message="请输入手机号：", check_re=r"^1[3-9]\d{9}$")
    logger.debug(f"手机号：{phone}")

    # 5. 输出信息
    print('*' * 50)
    print("您输入的信息如下：")
    print("用户名：" + username)
    print("昵称：" + nickname)
    print("密码：" + '*' * len(a_password))
    print("手机号：" + phone)
    print('*' * 50)
    # 6. 确认信息
    confirm = get_input(message="确认注册(Y)，取消注册(N)，重新注册(R)：",
                        check_re=r"^[YyNnRr]$")
    logger.debug(f"确认结果：{confirm}")

    # 如果用户确认注册，将用户的个人信息保存到文件中
    if confirm.lower() == 'y':
        # 计算用户 id
        try:
            user = Userinfo()
            user.username = username
            user.nickname = nickname
            user.password = a_password
            user.phone = phone
            UserinfoDAO.insert(user)

            logger.debug("完成注册，用户信息已保存")
            input("注册成功...按任意键继续")
            WelcomePage().show()
        except Exception as e:
            logger.exception(e)  # 会将 trace 写入日志
            input(str(e) + "...按任意键继续")
            page.show()
    elif confirm.lower() == 'n':
        # 放弃注册，回到欢迎页面
        WelcomePage().show()
    elif confirm.lower() == 'r':
        # 重新输入的时候，再次展示 register 页面的 show()
        page.show()
    else:
        # 为了健壮性
        print("您输入的指令不支持...请联系管理员")
        WelcomePage().show()


def do_login(page):
    logger.info("用户登录检查")
    username = get_input(message="请输入用户名：", warning="用户名不能为空")
    logger.debug(f"用户名：{username}")

    password = get_input(message="请输入密码：", warning="密码不能为空",
                         is_password=True)

    try:
        user = UserinfoDAO.select_one(username)
        logger.info(f"当前用户 {str(user)}")
        # 检查密码
        if user is None or\
                user.password != encrypt_password(password, username):
            raise PermissionError("用户名或密码错误")
        input("登录成功...按任意键继续")

        # 进入 homepage
        HomePage(user).show()
    except Exception as e:
        logger.exception(e)
        input(str(e) + "...按任意键重新输入")
        page.show()


def do_findpass(page):
    """找回密码"""
    username = get_input(message="请输入用户名：", check_re=r"^\w{3,16}$")
    logger.debug(f"用户名：{username}")

    user = UserinfoDAO.select_one(username)
    if user is None:
        print("用户不存在...按任意键继续")
        page.show()

    print(f"验证码发送到尾号为({user.phone[-4:]})的手机上，请注意查收...")
    random_code = get_input(message="请输入验证码：", check_re=r"^\d{6}$")  # 暂时随便输
    logger.debug(f"用户输入验证码 {random_code}")
    
    # 检查验证码的正确性，这里暂不实现

    # 输入新密码
    f_password = get_input(message="请输入新密码（6-12位）：",
                           warning="密码不能为空", is_password=True)
    logger.debug(f"输入新密码 {f_password}")
    # 确认新密码
    a_password = get_input(message="请确认新密码：",
                           warning="两次输入的密码不一致，请重新输入",
                           check_re=f"^{f_password}$", is_password=True)
    logger.debug(f"确认新密码 {a_password}")

    # 更新用户密码
    user.password = f_password
    UserinfoDAO.update(user)  # 为了辨识，user 为实参，p_user 为形参
    input("修改密码成功...按任意键继续")
    page.show()


@logincheck
def do_changepass(page):
    # 输入旧密码
    o_password = get_input(message="请输入旧密码：",
                           warning="密码不能为空", is_password=True)
    if page.user.password != encrypt_password(o_password, page.user.username):
        input("密码错误...按任意键继续")
        page.show()
    # 输入新密码
    f_password = get_input(message="请输入新密码（6-12位）：",
                           warning="密码不能为空", is_password=True)
    # 确认新密码
    a_password = get_input(message="请确认新密码：",
                           warning="两次输入的密码不一致，请重新输入",
                           check_re=f"^{f_password}$", is_password=True)
    logger.debug(f"确认密码：{a_password}")
    page.user.password = a_password
    UserinfoDAO.update(page.user)
    input("密码修改成功...按任意键继续")
    page.show()


@logincheck
def do_changename(page):
    # 输入密码
    password = get_input(message="请输入密码：",
                         warning="密码不能为空", is_password=True)
    if page.user.password != encrypt_password(password, page.user.username):
        input("密码错误...按任意键继续")
        page.show()
    # 输入新昵称
    nickname = get_input(message="请输入昵称（1-10位）：",
                         check_re=r"^\S{1,10}$")
    logger.debug(f"昵称：{nickname}")
    page.user.nickname = nickname
    UserinfoDAO.update(page.user)
    input("昵称修改成功...按任意键继续")
    page.show()


@logincheck
def user_info(page):
    """个人用户信息页面"""
    UserinfoPage(user=page.user, home=page, prev=page).show()


@logincheck
def user_logout(page):
    """用户注销"""
    page.user = None
    WelcomePage().show()


@authcheck
def user_readerlist(page):
    print("进入读者管理页面")
    ReaderListPage(user=page.user, home=page, prev=page).show()


@authcheck
def do_readerlist(page):
    command = get_input(message="查询条件：用户名(u)，手机号(p)，读者详情(i)，回车查全部：",
                        check_re=r"^[upiUPI]$", empty=True)
    logger.debug(command)

    if not command or command.lower() != 'i':
        if command.lower() == 'u':
            username = get_input(message="请输入用户名：")
        if command.lower() == 'p':
            phone = get_input(message="请输入手机号：")
        print('-' * page.MESSAGE_MAX_LEN)
        print("{:4}|{:9}|{:10}|{}".format("编号", "用户名", "昵称", "手机号"))
        print('-' * page.MESSAGE_MAX_LEN)
        
        readers = UserinfoDAO.select(level="reader")
        count = 0
        for reader in readers:
            if command.lower() == 'u' and reader.username != username:
                continue
            if command.lower() == 'p' and reader.phone != phone:
                continue
            nickname = reader.nickname
            nickname_size = 12 - (len(nickname.encode("gbk")) - len(nickname))
            print(f"{reader.userid:<6}|{reader.username:12}|"
                  f"{nickname:{nickname_size}}|{reader.phone:11}")
            count += 1
        print('-' * page.MESSAGE_MAX_LEN)
        print(f"共 {count} 条数据")

    reader_id = get_input(message="查看用户详情，请输入用户编号：",
                          check_re=r"^\d+$", empty=True)
    if reader_id:
        logger.debug(reader_id)
        reader = UserinfoDAO.select_one(p_userid=int(reader_id))
        if reader is None:
            print(f"读者 {reader_id} 不存在...按任意键继续")
            page.show()
        else:
            # 进入读者详情页
            ReaderinfoPage(user=page.user, reader=reader,
                           home=page.home_page, prev=page).show()
    else:
        page.show()


@authcheck
def do_set_admin(page):
    """设为管理员"""
    reader = page.reader
    confirm = get_input(message="确认(Y), 取消(N)：", check_re=r"^[ynYN]$")
    if confirm.lower() == 'y':
        reader.is_admin = True
        UserinfoDAO.update(reader)
        input("设置成功...按任意键继续")
    page.show()
