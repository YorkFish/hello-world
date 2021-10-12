# coding: utf-8
"""
图书浏览

author: York
date: 2021-10-07
"""

from pages.SuperPage import SuperPage


class BookListPage(SuperPage):
    PAGE_MESSAGE = [
        "---图书浏览---",
        "在册图书({len(BookinfoDAO.select(p_state='normal'))})册",
        "借阅图书({len(BookinfoDAO.select(p_is_borrow=True))})册"
    ]

    PAGE_ACTIONS = [{
        "KEY": "n",
        "DESC": "登记图书",
        "ACTION": "BookActions.book_register"
    }, {
        "KEY": "s",
        "DESC": "查询",
        "ACTION": "BookActions.do_booklist"
    }, {
        "KEY": "u",
        "DESC": "借阅",
        "ACTION": "BookActions.do_borrow"
    }, {
        "KEY": "m",
        "DESC": "修改",
        "AUTH": "admin",
        "ACTION": "BookActions.do_modify"
    }, {
        "KEY": "u",
        "DESC": "删除",
        "AUTH": "admin",
        "ACTION": "BookActions.do_delete"
    }]
