# coding: utf-8
"""
author: York
date: 2021-09-19
"""

import logging
import os

current_path = os.path.abspath(__file__)
log_file = os.path.join(os.path.abspath(os.path.dirname(current_path)),
                        "debug.log")
fmt = "%(asctime)s|%(levelname)8s|%(filename)20s:%(lineno)3s|%(message)s"
logging.basicConfig(level=logging.DEBUG, filename=log_file, format=fmt)
# logging.debug("debug")
# logging.info("infomation")
# logging.warning("warning")
# logging.error("error")
# logging.critical("critical")
logger = logging.getLogger()
