#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint


CWD = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.sep.join([CWD, '..'])
SETTING_DIR = os.path.sep.join([PROJ_DIR, 'settings'])


class run_settings():
    # False to run in console
    display_video_window = True

    width_lane = 100
    width_DVL = 100
    T_HDist = 60
    T_VDist = 100
    T_s = 0.3

    pause_between_screen = 3



    def __init__(self):
        pass
