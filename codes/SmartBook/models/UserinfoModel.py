# coding: utf-8
"""
author: York
date: 2021-09-25
"""

import os
from api.PublicApi import *
from applogger import logger
from models.SuperModel import SuperModel


class Userinfo:
    """静态的数据模型"""
    def __init__(self, userid=None, username=None, password=None,
                 nickname=None, phone=None, is_admin=False, state=None,
                 create_date=None, last_date=None):
        """
        Userinfo model 类
        对应文件中的一行
        """
        self.userid = userid
        self.username = username
        self.password = password
        self.nickname = nickname
        self.phone = phone
        self.is_admin = is_admin
        self.state = state
        self.create_date = create_date
        self.last_date = last_date

    def properties(self):
        return [str(self.userid), self.username, self.password, self.nickname,
                self.phone, str(self.is_admin), self.state, self.create_date,
                self.last_date]

    def to_file_line(self):
        return SuperModel.FILE_SEPARATOR.join(self.properties()) + '\n'

    def __str__(self):
        return f"Userinfo:({', '.join(self.properties())})"

    def __repr__(self):
        return self.__str__()

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        self.__is_admin = value == "True" or value is True


class UserinfoDAO:
    """
    Userinfo 数据访问对象
    DAO: data access object
    """
    current_path = os.path.abspath(__file__)
    FILE_NAME = os.path.join(os.path.abspath(os.path.dirname(current_path)),
                             "Userinfo.dbx")

    @staticmethod
    def insert(p_user):
        if os.path.exists(UserinfoDAO.FILE_NAME):
            with open(UserinfoDAO.FILE_NAME, 'r', encoding="utf-8") as rf:
                filelines = rf.readlines()
            # 检查用户名的重复性
            for line in filelines:
                if line.split(SuperModel.FILE_SEPARATOR)[1] == p_user.username:
                    raise NameError("用户名已注册")
            p_user.userid = len(filelines) + 1
        else:
            p_user.userid = 1

        p_user.state = '0'
        p_user.is_admin = False
        today = get_today()
        p_user.create_date = today
        p_user.last_date = today
        p_user.password = encrypt_password(p_user.password, p_user.username)
        with open(UserinfoDAO.FILE_NAME, 'a',
                  encoding=SuperModel.FILE_ENCODING) as af:
            af.write(p_user.to_file_line())

    @staticmethod
    def select(level=None):
        res = []
        if os.path.exists(UserinfoDAO.FILE_NAME):
            with open(UserinfoDAO.FILE_NAME, 'r',
                      encoding=SuperModel.FILE_ENCODING) as rf:
                filelines = rf.readlines()
            for line in filelines:
                fields = line.split(SuperModel.FILE_SEPARATOR)
                user = Userinfo()
                user.userid = int(fields[0])
                user.username = fields[1]
                user.password = fields[2]
                user.nickname = fields[3]
                user.phone = fields[4]
                user.is_admin = fields[5]
                user.state = fields[6]
                user.create_date = fields[7]
                user.last_date = fields[8].rstrip()

                if level == "reader" and user.is_admin:
                    continue  # 若只要读者，则跳过管理员
                res.append(user)
        return res

    # 入口传进来的变量加一个标记，如 p 打头
    @staticmethod
    def select_one(p_username=None, p_userid=None):
        users = UserinfoDAO.select()
        for user in users:
            if user.username == p_username:
                return user
            if user.userid == p_userid:
                return user
        return None

    @staticmethod
    def update(p_user):
        if p_user and p_user.userid > 0:
            users = UserinfoDAO.select()
            for i_user in users:
                if i_user.userid == p_user.userid:
                    i_user.username = p_user.username
                    i_user.password = encrypt_password(p_user.password,
                                                       p_user.username)
                    i_user.nickname = p_user.nickname
                    i_user.phone = p_user.phone
                    i_user.is_admin = p_user.is_admin
                    i_user.state = p_user.state
                    i_user.create_date = p_user.create_date
                    i_user.last_date = p_user.last_date

                    logger.info("update userinfo:")
                    logger.info(i_user)
                    break

            with open(UserinfoDAO.FILE_NAME, 'w',
                      encoding=SuperModel.FILE_ENCODING) as wf:
                for u in users:
                    wf.write(u.to_file_line())
        else:
            raise ValueError("user 参数错误.")
