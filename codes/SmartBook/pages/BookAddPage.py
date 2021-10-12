# coding: utf-8
"""
图书登记

author: York
date: 2021-10-07
"""

from pages.SuperPage import SuperPage


class BookAddPage(SuperPage):
    PAGE_MESSAGE = [
        "---图书登记---"
    ]

    PAGE_ACTIONS = [{
        "KEY": "r",
        "DESC": "登记图书",
        "ACTION": "BookActions.do_register"
    }]
