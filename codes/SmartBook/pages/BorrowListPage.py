# coding: utf-8
"""
借阅清单

author: York
date: 2021-10-08
"""

from pages.SuperPage import SuperPage


class BorrowListPage(SuperPage):
    PAGE_MESSAGE = [
        "---借阅清单---"
    ]

    PAGE_ACTIONS = [{
        "KEY": "s",
        "DESC": "查询",
        "ACTION": "BookActions.do_borrowlist"
    }, {
        "KEY": "r",
        "DESC": "归还",
        "ACTION": "BookActions.do_return"
    }]
