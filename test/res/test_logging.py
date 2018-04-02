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

PROJ_HOME = os.path.sep.join([TEST_HOME, '..'])
SOURCE_DIR = os.path.sep.join([PROJ_HOME, 'source'])
RES_DIR = os.path.sep.join([SOURCE_DIR, 'res'])
SRC_DIR = os.path.sep.join([SOURCE_DIR, 'src'])


sys.path += [TEST_SRC_DIR, TEST_RES_DIR, SRC_DIR, RES_DIR]

import const

const.init_logging()
