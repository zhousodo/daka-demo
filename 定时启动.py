# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     77777777
   Description :
   Author :       aikt409
   date：          2020/5/19
-------------------------------------------------
   Change Activity:
                   2020/5/19:
-------------------------------------------------
"""
from datetime import datetime

__author__ = 'aikt409'
import time, os
import logging
def re_exe(cmd_list,inc):
    while True:
        ts_start = datetime.now()
        if ts_start.hour== 10:#每天10点定时运行task脚本
            for cmd in cmd_list:
                os.system(cmd)

        time.sleep(inc)
        print(ts_start.hour)
        print(ts_start)

cmd_list = ['python --version']
re_exe(cmd_list, 24)