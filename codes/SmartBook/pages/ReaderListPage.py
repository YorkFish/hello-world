# coding: utf-8
"""
author: York
date: 2021-10-02
"""

from pages.SuperPage import SuperPage


class ReaderListPage(SuperPage):
    PAGE_MESSAGE = [
        "---读者管理---",
        "注册读者{len(UserinfoDAO.select(level='reader'))}",
    ]

    PAGE_ACTIONS = [{
        "KEY": "rl",
        "DESC": "读者列表",
        "ACTION": "UserActions.do_readerlist"
    }]
