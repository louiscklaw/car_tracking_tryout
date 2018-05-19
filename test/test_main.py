#!/usr/bin/env python
# coding:utf-8

"""
Helloworld boilder plate

Naming style guideline
# https://google.github.io/styleguide/pyguide.html
# http://www.sphinx-doc.org/en/master/ext/napoleon.html#docstring-sections

PYTHON UNITTEST:
# https://docs.python.org/3/library/unittest.html

"""

import os
import sys
import logging
import traceback
import subprocess
import shlex

from pprint import pprint

import unittest

CWD = os.path.dirname(os.path.abspath(__file__))
TEST_HOME = CWD
TEST_SRC_DIR = os.path.sep.join([TEST_HOME, 'src'])
TEST_RES_DIR = os.path.sep.join([TEST_HOME, 'res'])

PROJ_HOME = os.path.sep.join([TEST_HOME, '..'])
SOURCE_DIR = os.path.sep.join([PROJ_HOME, 'source'])
RES_DIR = os.path.sep.join([SOURCE_DIR, 'res'])
SRC_DIR = os.path.sep.join([SOURCE_DIR, 'src'])

sys.path += [TEST_SRC_DIR, TEST_RES_DIR, SRC_DIR, RES_DIR]


class test_setting():
    DOCKER_WORK_DIR = '/workdir'
    DOCKER_TEST_DIR = os.path.sep.join([DOCKER_WORK_DIR, 'test'])
    DOCKER_TEST_DATA_DIR = os.path.sep.join([DOCKER_TEST_DIR, 'test_data'])

    DOCKER_SOURCE_DIR = os.path.sep.join([DOCKER_WORK_DIR, 'source'])
    TEST_SCRIPT = os.path.sep.join([DOCKER_SOURCE_DIR, 'VehicleCounting.py'])


class RUN_ENV:
    def get_bin(bin_name):
        return subprocess.check_output(['which', bin_name]).strip()

    DOCKER_BIN_PATH = get_bin('docker')
    PYTHON_BIN_PATH = get_bin('python')


class ERROR_TEXTS:
    ERROR_CLEANUP_DOCKER = 'error during cleanup docker'
    ERROR_CREATE_DOCKER = 'error during create docker'
    ERROR_RECREATE_DOCKER = 'error during recreate docker'
    ERROR_COPY_SOURCE_DOCKER = 'error during copy source to docker'


class STATUS_TEXTS:
    TEXT_COPY_SOURCE_DOCKER = 'coping source to docker'
    TEXT_RECREATE_DOCKER = 'recreate docker'


class docker_commands:
    TEST_IMAGE_NAME = 'test_ubuntu_opencv'

    def __init__(self):
        pass

    def get_docker_exec_command(self, test_command):

        return '{} exec {} {}'.format(RUN_ENV.DOCKER_BIN_PATH, self.TEST_IMAGE_NAME, test_command)

    def get_killall_command(self):
        return '{} kill {}'.format(RUN_ENV.DOCKER_BIN_PATH, self.TEST_IMAGE_NAME)

    def get_rmall_command(self):
        return '{} rm {}'.format(RUN_ENV.DOCKER_BIN_PATH, self.TEST_IMAGE_NAME)

    def get_create_command(self):
        return '{} create --name {} -p 5901:5901 logickee/ubuntu_opencv'.format(RUN_ENV.DOCKER_BIN_PATH, self.TEST_IMAGE_NAME)

    def get_start_command(self):
        return '{} start {} '.format(RUN_ENV.DOCKER_BIN_PATH, self.TEST_IMAGE_NAME)

    def get_copy_source_command(self):
        return '{} cp ./ {}:/workdir'.format(RUN_ENV.DOCKER_BIN_PATH, self.TEST_IMAGE_NAME)

    def run_command(self, commands):
        for command in commands:
            print('running command {}'.format(command))
            subprocess.check_output(command, shell=True)

    def docker_cleanup(self):
        try:
            [self.run_command([
                self.get_killall_command(),
                self.get_rmall_command()
            ])]

        except Exception as e:
            print(ERROR_TEXTS.ERROR_CLEANUP_DOCKER)

    def docker_create(self):
        try:
            [self.run_command([
                self.get_create_command(),
                self.get_start_command()
            ])]
        except Exception as e:
            print(ERROR_TEXTS.ERROR_CREATE_DOCKER)

    def docker_copy_source(self):
        try:
            print(STATUS_TEXTS.TEXT_COPY_SOURCE_DOCKER)
            [self.run_command([
                self.get_copy_source_command()
            ])]
        except Exception as e:
            print(ERROR_TEXTS.ERROR_COPY_SOURCE_DOCKER)

    def docker_recreate(self):
        try:
            print(STATUS_TEXTS.TEXT_RECREATE_DOCKER)
            self.docker_cleanup()
            self.docker_create()
        except Exception as e:
            print(ERROR_TEXTS.ERROR_RECREATE_DOCKER)


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
        # init docker_commands object for getting docker command
        self.docker_commands = docker_commands()

    def tearDown(self):
        print('teardown (car_track) test')

    # def test_init_logging(self):
    #     import const
    #     const.init_logging()

    def car_count_using_video(self, expecting_car_number, video_file):
        self.docker_commands.docker_recreate()
        self.docker_commands.docker_copy_source()

        test_command = '{PYTHON_BIN_PATH} {test_script} -vid {video_file}'.format(
            PYTHON_BIN_PATH=RUN_ENV.PYTHON_BIN_PATH
            test_script=test_setting.TEST_SCRIPT,
            video_file=video_file)
        # command = 'docker exec test_ubuntu_opencv ls'

        docker_exec_command = docker_command(test_command).get_docker_exec_command()

        result = subprocess.check_output(docker_exec_command, shell=True)
        result = result.decode('utf-8')

        text_vehicle_counted = 'total number of vehicles: {}\n'.format(expecting_car_number)

        self.assertIn(text_vehicle_counted, result, 'the counting not correct, result from output {}'.format(result))
        # docker_cleanup()

    def test_default_video(self):
        test_set = {
            'origional_test.mp4': "52",
            # 'VID_20180402_154210.mp4': "128",
            'VID_20180407_175555_small.mp4': '34',
        }

        for video_file, no_of_car in test_set.items():
            text_testing_video = 'testing with video {}'.format(video_file)
            print(text_testing_video)

            video_file = os.path.sep.join([test_setting.DOCKER_TEST_DATA_DIR, video_file])

            self.car_count_using_video(no_of_car, video_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
