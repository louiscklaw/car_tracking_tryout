#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
import subprocess
import shlex

from pprint import pprint

import unittest
# https://docs.python.org/3/library/unittest.html


CWD = os.path.dirname(os.path.abspath(__file__))
TEST_HOME = CWD
TEST_SRC_DIR = os.path.sep.join([TEST_HOME, 'src'])
TEST_RES_DIR = os.path.sep.join([TEST_HOME, 'res'])

PROJ_HOME = os.path.sep.join([TEST_HOME, '..'])
SOURCE_DIR = os.path.sep.join([PROJ_HOME, 'source'])
RES_DIR = os.path.sep.join([SOURCE_DIR, 'res'])
SRC_DIR = os.path.sep.join([SOURCE_DIR, 'src'])


sys.path += [TEST_SRC_DIR, TEST_RES_DIR, SRC_DIR, RES_DIR]


TEST_IMAGE_NAME = 'test_ubuntu_opencv'
KILLALL_DOCKER = 'docker kill {}'.format(TEST_IMAGE_NAME)
RMALL_DOCKER = 'docker rm {}'.format(TEST_IMAGE_NAME)
CREATE_DOCKER = 'docker create --name {} -p 5901:5901 logickee/ubuntu_opencv'.format(TEST_IMAGE_NAME)
START_DOCKER = 'docker start {} '.format(TEST_IMAGE_NAME)
COPY_SOURCE_DOCKER = 'docker cp ./ {}:/workdir'.format(TEST_IMAGE_NAME)


class test_setting():
    DOCKER_WORK_DIR = '/workdir'
    DOCKER_TEST_DIR = os.path.sep.join([DOCKER_WORK_DIR, 'test'])
    DOCKER_TEST_DATA_DIR = os.path.sep.join([DOCKER_TEST_DIR, 'test_data'])

    DOCKER_SOURCE_DIR = os.path.sep.join([DOCKER_WORK_DIR, 'source'])
    TEST_SCRIPT = os.path.sep.join([DOCKER_SOURCE_DIR, 'VehicleCounting.py'])


def run_command(commands):
    for command in commands:
        print('running command {}'.format(command))
        subprocess.check_output(command, shell=True)


def docker_cleanup():
    ERROR_CLEANUP_DOCKER = 'error during cleanup docker'
    try:
        [run_command([KILLALL_DOCKER, RMALL_DOCKER])]

    except Exception as e:
        print(ERROR_CLEANUP_DOCKER)


def docker_create():
    ERROR_CREATE_DOCKER = 'error during create docker'
    try:
        [run_command([CREATE_DOCKER, START_DOCKER])]
    except Exception as e:
        print(ERROR_CREATE_DOCKER)


def docker_recreate():
    ERROR_RECREATE_DOCKER = 'error during recreate docker'
    try:
        print('recreate docker')
        docker_cleanup()
        docker_create()
    except Exception as e:
        print(ERROR_RECREATE_DOCKER)


def docker_copy_source():
    TEXT_COPY_SOURCE_DOCKER = 'coping source to docker'
    ERROR_COPY_SOURCE_DOCKER = 'error during copy source to docker'
    try:
        print(TEXT_COPY_SOURCE_DOCKER)
        run_command([COPY_SOURCE_DOCKER])
    except Exception as e:
        print(ERROR_COPY_SOURCE_DOCKER)


def setUpModule():
    print('setup (car_track) module')


def tearDownModule():
    print('teardown (car_track) module')


class Test_car_track(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setup (car_track) class')

    @classmethod
    def tearDownClass(cls):
        print('teardown (car_track) class')

    def setUp(self):
        print('setup (car_track) test')

    def tearDown(self):
        print('teardown (car_track) test')

    # def test_init_logging(self):
    #     import const
    #     const.init_logging()

    def car_count_using_video(self, expecting_car_number, video_file):
        # docker_recreate()
        # docker_copy_source()

        test_command = 'python {test_script} -vid {video_file}'.format(
            test_script=test_setting.TEST_SCRIPT,
            video_file=video_file)
        # command = 'docker exec test_ubuntu_opencv ls'

        result = subprocess.check_output(test_command, shell=True)
        result = result.decode('utf-8')

        self.assertIn('total number of vehicles: {}\n'.format(expecting_car_number), result, 'the counting not correct, result from output {}'.format(result))

        # docker_cleanup()



    def test_default_video(self):
        test_set = {
            'origional_test.mp4': "52",
            # 'VID_20180402_154210.mp4': "128"
        }

        for video_file, no_of_car in test_set.items():
            print('testing with video {}'.format(video_file))
            video_file = os.path.sep.join([test_setting.DOCKER_TEST_DATA_DIR, video_file])
            self.car_count_using_video(no_of_car, video_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
