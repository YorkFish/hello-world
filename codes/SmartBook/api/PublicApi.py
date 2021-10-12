# coding: utf-8
"""
模块描述：
系统的公共方法

author: York
date: 2021-09-25
"""

# import datetime
import hashlib
import os
import re
from getpass import getpass
from applogger import logger


def encrypt_password(password, username):
    b_pwd = (password + username).encode("utf-8")
    return hashlib.md5(b_pwd).hexdigest()


def get_today():
    # return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "yyyy-mm-dd"


def get_input(message, warning="输入有误，请重新输入",
              check_re=None, is_password=False, empty=False):
    while True:
        ipt = input(message) if not is_password else getpass(message)
        if empty and ipt == '':
            break
        if ipt and (True if not check_re else re.match(check_re, ipt)):
            break
        else:
            print(warning)
    return ipt


def clear_screen():
    os.system("cls")


# 检查管理员登录权限
def authcheck(func):
    def wrapper(page):
        logger.info("管理员权限检查：")
        logger.info(page.user)
        logger.info(page)
        
        if not page.user.is_admin:
            raise PermissionError("权限不足")
        func(page)
    return wrapper


# 登录检查
def logincheck(func):
    def wrapper(page):
        try:
            logger.info("登录检查：")
            logger.info(page.user)
            logger.info(page)
            
            if page.user is None:
                raise PermissionError("请登录")
            func(page)
        except Exception as e:
            logger.exception(e)
            print(e)
    return wrapper
