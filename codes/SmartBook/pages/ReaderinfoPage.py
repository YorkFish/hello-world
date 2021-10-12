# coding: utf-8
"""
读者详情页

author: York
date: 2021-10-06
"""

from pages.SuperPage import SuperPage


class ReaderinfoPage(SuperPage):
    PAGE_MESSAGE = [
        "",
        "---读者详情---",
        "编号：{self.reader.userid}",
        "用户名：{self.reader.username}",
        "手机号：{self.reader.phone}",
        ""
    ]

    PAGE_ACTIONS = [{
        "KEY": "a",
        "DESC": "设为管理员",
        "ACTION": "UserActions.do_set_admin"
    }, {
        "KEY": "s",
        "DESC": "借阅清单",
        "ACTION": "BookActions.book_reader_borrowlist"
    }]
