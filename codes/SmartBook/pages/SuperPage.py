# coding: utf-8
"""
模块描述：
所有页面的父类

author: York
date: 2021-09-25
"""

import re
from api.PublicApi import *
from applogger import logger
from models.UserinfoModel import UserinfoDAO
from models.BookinfoModel import BookinfoDAO


class SuperPage:
    """
    封装所有页面的公共方法
    """
    MESSAGE_MAX_LEN = 60

    def __init__(self, user=None, reader=None, home=None, prev=None):
        self.user = user
        self.reader = reader
        self.home_page = home
        self.prev_page = prev

    def show(self):
        clear_screen()
        if self.user:
            print(f"当前用户：{self.user.username}({self.user.nickname})，"
                  f"系统日期：{get_today()}")

        print('*' * SuperPage.MESSAGE_MAX_LEN)
        for msg in self.PAGE_MESSAGE:
            t = msg
            for ps in re.findall(r"\{.+?\}", t):
                msg = msg.replace(ps, str(eval(ps[1:-1])))
            size = SuperPage.MESSAGE_MAX_LEN -\
                   (len(msg.encode("utf-8")) - len(msg)) // 2
            print("{0:^{1}s}".format(msg, size))
        print('*' * SuperPage.MESSAGE_MAX_LEN)

        self.do_action()

    def do_action(self):
        if len(self.PAGE_ACTIONS) == 0:
            logger.warning("页面未定义actions")
            return

        elif len(self.PAGE_ACTIONS) == 1:
            action_str = self.PAGE_ACTIONS[0]["ACTION"]
        else:
            command_line = ""
            for action in self.PAGE_ACTIONS:
                if "AUTH" in action and not self.user.is_admin:
                    continue
                if command_line:
                    command_line += '，'
                command_line += f'{action["DESC"]}({action["KEY"].upper()})'
            logger.debug(command_line)

            print("您可以选择如下操作：")
            if self.home_page:
                print("首页(H)，", end='')
            if self.prev_page and self.prev_page is not self.home_page:
                print("上一页(B)，", end='')
            print(command_line)

            actions = [d["KEY"] for d in self.PAGE_ACTIONS] + ['h', 'b']
            while True:
                command = input("请输入：")
                if command.lower() in actions:
                    logger.debug(f"用户输入的命令是：{command}")
                    break
                else:
                    print("输入有误，请重新输入...")

            # 回首页
            if command.lower() == 'h':
                self.home_page.show()
            if command.lower() == 'b':
                self.prev_page.show()

            # 根据用户的指令获取 action 字符串
            for action in self.PAGE_ACTIONS:
                if command.lower() == action["KEY"].lower():
                    action_str = action["ACTION"]
                    logger.debug("找到指令：" + action_str)
                    break
        # 反射调用 登录、注册、退出等方法
        module, funcname = action_str.split('.')
        module = __import__("actions." + module, fromlist=True)
        if hasattr(module, funcname):
            logger.info(f">>> action: {action_str}")
            action_func = getattr(module, funcname)
            action_func(self)
        else:
            print(f"指令{command}的{funcname}方法未定义")
