#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint


CWD = os.path.dirname(os.path.abspath(__file__))
PROJ_HOME = os.path.sep.join([CWD, '..'])
SRC_DIR = os.path.sep.join([PROJ_HOME, 'src'])
RES_DIR = os.path.sep.join([PROJ_HOME, 'res'])

sys.path += [SRC_DIR, RES_DIR]

import const


const.init_logging()
