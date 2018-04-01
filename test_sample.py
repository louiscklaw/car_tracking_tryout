#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint


import unittest
# https://docs.python.org/3/library/unittest.html


class testclass(object):
    """testclass"""
    TEST_TOPIC1 = 'test topic1'
    TEST_SAMPLE_STATUS1 = 'STEPstatus1'
    TEST_SAMPLE_STATUS2 = 'STEPstatus2'
    TEST_SAMPLE_STATUS3 = 'STEPstatus3'


class StatusText(object):
    """StatusText"""
    TEST_TOPIC1 = 'test topic1'
    SAMPLE_STATUS1 = 'sample status1'
    SAMPLE_STATUS2 = 'sample status2'


class StatusText(object):
    TEST_TOPIC1 = 'test topic1'
    SAMPLE_STATUS1 = 'sample status1'
    SAMPLE_STATUS2 = 'sample status2'


class ErrorText(object):
    """ErrorText"""
    ERROR_TOPIC1 = 'error topic1'
    ERROR_SAMPLE_ERROR1 = 'error 1'
    ERROR_SAMPLE_ERROR2 = 'error 2'


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

    def test_topic(self):
        print("hello (topic)")
        self.assertEqual(1 / 0, 1)


class ResultCollector(object):
    def upload_result(result):
        print('uploading result')
        print('dump of incoming result: {}'.format(result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
