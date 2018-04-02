#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

CWD = os.path.dirname(os.path.abspath(__file__))
TEST_HOME = os.path.sep.join([CWD, '..'])
TEST_SRC_DIR = os.path.sep.join([TEST_HOME, 'src'])
TEST_RES_DIR = os.path.sep.join([TEST_HOME, 'res'])

sys.path += [TEST_SRC_DIR, TEST_RES_DIR]

import const

const.init_logging()
