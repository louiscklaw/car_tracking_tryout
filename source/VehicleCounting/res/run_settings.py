#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint


class run_settings():
    # False to run in console
    display_video_window = False

    width_lane = 100
    width_DVL = 100
    T_HDist = 60
    T_VDist = 100
    T_s = 0.3

    def __init__(self):
        pass
