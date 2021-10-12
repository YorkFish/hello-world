# coding: utf-8
"""
模块描述：
系统公共 actions 方法

author: York
date: 2021-09-29
"""

import sys
from applogger import logger


def sys_exit(page):
    print("再见，欢迎下次使用...")
    logger.info("用户退出系统")
    sys.exit(0)
