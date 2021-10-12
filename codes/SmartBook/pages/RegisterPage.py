# coding: utf-8
"""
author: York
date: 2021-09-25
"""

from pages.SuperPage import SuperPage


class RegisterPage(SuperPage):
    PAGE_MESSAGE = [
        "",
        "用户注册",
        ""
    ]

    PAGE_ACTIONS = [{
        "KEY": "r",
        "DESC": "注册",
        "ACTION": "UserActions.do_register"
    }]
