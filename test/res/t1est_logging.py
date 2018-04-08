#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
import subprocess
import shlex

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
import unittest
# https://docs.python.org/3/library/unittest.html


def setUpModule():
    print('setup (topic) module')


def tearDownModule():
    print('teardown (topic) module')


class Test_topic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setup (topic) class')

    @classmethod
    def tearDownClass(cls):
        print('teardown (topic) class')

    def setUp(self):
        print('setup (topic) test')

    def tearDown(self):
        print('teardown (topic) test')

    def test_init_logging(self):

        const.init_logging()


if __name__ == '__main__':
    unittest.main(verbosity=2)
