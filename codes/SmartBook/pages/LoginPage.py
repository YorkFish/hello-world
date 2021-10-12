# coding: utf-8
"""
author: York
date: 2021-09-26
"""

from pages.SuperPage import SuperPage


class LoginPage(SuperPage):
    PAGE_MESSAGE = [
        "用户登录",
        "---请输入用户名和密码---"
    ]

    PAGE_ACTIONS = [{
        "KEY": "l",
        "DESC": "登录",
        "ACTION": "UserActions.do_login"
    }]
