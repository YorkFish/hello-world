# coding: utf-8
"""
模块描述：
欢迎页

author: York
date: 2021-09-25
"""

from pages.SuperPage import SuperPage


class WelcomePage(SuperPage):
    PAGE_MESSAGE = [
        "",
        "欢迎来到，",
        "图书管理系统(SmartBook)",
        "版本号：V0.1",
        "系统日期：YYYY年MM月DD日",
        ""
    ]

    PAGE_ACTIONS = [{
        "KEY": "l",
        "DESC": "登录",
        "ACTION": "UserActions.user_login"
    }, {
        "KEY": "r",
        "DESC": "注册",
        "ACTION": "UserActions.user_register"
    }, {
        "KEY": "f",
        "DESC": "找回密码",
        "ACTION": "UserActions.do_findpass"
    }, {
        "KEY": "q",
        "DESC": "退出",
        "ACTION": "PublicActions.sys_exit"
    }]
