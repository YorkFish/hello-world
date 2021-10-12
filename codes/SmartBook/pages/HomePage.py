# coding: utf-8
"""
author: York
date: 2021-09-26
"""

from pages.SuperPage import SuperPage


class HomePage(SuperPage):
    PAGE_MESSAGE = [
        "",
        "您好，{self.user.nickname}，您是第{self.user.userid}个读者",
        "欢迎来到图书管理系统(SmartBook)",
        "在册等级图书(300)，借阅图书(5)",
        "上次登录：{self.user.last_date}",
        ""
    ]

    PAGE_ACTIONS = [{
        "KEY": "p",
        "DESC": "个人信息",
        "ACTION": "UserActions.user_info"
    }, {
        "KEY": "l",
        "DESC": "图书浏览",
        "ACTION": "BookActions.book_list"
    }, {
        "KEY": "u",
        "DESC": "读者管理",
        "AUTH": "admin",
        "ACTION": "UserActions.user_readerlist"
    }, {
        "KEY": "s",
        "DESC": "借阅清单",
        "ACTION": "BookActions.book_borrowlist"
    }, {
        "KEY": "e",
        "DESC": "注销",
        "ACTION": "UserActions.user_logout"
    }]
