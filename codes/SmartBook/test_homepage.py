# coding: utf-8
"""
author: York
date: 2021-10-06
"""

from models.UserinfoModel import UserinfoDAO
from pages.HomePage import HomePage

user = UserinfoDAO.select_one("york")
# user = UserinfoDAO.select_one("luke")
HomePage(user).show()
