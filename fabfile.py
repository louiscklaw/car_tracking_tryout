#!/usr/bin/env python

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

import time

DOCKER_DIR = './docker'


docker_settings = {
    'DOCKER_DIR': DOCKER_DIR
}

TEST_IMAGE_NAME = 'test_ubuntu_opencv'
KILLALL_DOCKER = 'docker kill {}'.format(TEST_IMAGE_NAME)
RMALL_DOCKER = 'docker rm {}'.format(TEST_IMAGE_NAME)
CREATE_DOCKER = 'docker create --name {} -p 5901:5901 logickee/ubuntu_opencv'.format(TEST_IMAGE_NAME)
START_DOCKER = 'docker start   {}  '.format(TEST_IMAGE_NAME)


from fabric.colors import *


class test_setting():
    DOCKER_WORK_DIR = '/workdir'
    DOCKER_TEST_DIR = os.path.sep.join([DOCKER_WORK_DIR, 'test'])
    DOCKER_TEST_DATA_DIR = os.path.sep.join([DOCKER_TEST_DIR, 'test_data'])

    DOCKER_SOURCE_DIR = os.path.sep.join([DOCKER_WORK_DIR, 'source'])
    TEST_SCRIPT = os.path.sep.join([DOCKER_SOURCE_DIR, 'VehicleCounting.py'])


def print_status(text): print(green(text))


def print_warnings(text): print(yellow(text))


def print_error(text): print(red(text))


from multiprocessing import Pool


def threaded_local(command):
    return local(command)


@task
def build():
    docker_build_commands = '''
docker build -t="logickee/ubuntu_16_04_gnome"  -f ./docker/dockerfile.ubuntu_gnome_16_04 {DOCKER_DIR}
docker build -t="logickee/ubuntu_opencv"  -f ./docker/dockerfile.opencv {DOCKER_DIR}
'''.format(**docker_settings)

    docker_push_commands = '''
docker push logickee/ubuntu_16_04_gnome
docker push logickee/ubuntu_opencv
    '''

    for docker_command in docker_build_commands.split('\n'):
        local(docker_command)

    p = Pool(5)
    p.map(threaded_local, docker_push_commands.split('\n'))


@task
def sync_proj_files():
    # local('docker cp ./source/VehicleCounting {}:/'.format(TEST_IMAGE_NAME))
    local('docker cp ./ {}:/workdir'.format(TEST_IMAGE_NAME))


def docker_clear_stage():
    with settings(warn_only=True):
        [local(docker_command) for docker_command in [
            KILLALL_DOCKER, RMALL_DOCKER
        ]]


@task
def up():
    docker_clear_stage()

    with settings(warn_only=True):
        [local(docker_command) for docker_command in [
            CREATE_DOCKER, START_DOCKER
        ]]

    # local('docker create --name {} -p 5901:5901 logickee/ubuntu_opencv'.format(TEST_IMAGE_NAME))

    # local('docker start   {}  '.format(TEST_IMAGE_NAME))


def test_start():
    up()
    sync_proj_files()


def test_end(debug):
    TEXT_DEBUG_ACTIVE = 'debug active, ignore delete docker'
    TEXT_CLEAR_CONTAINER = 'cleaning container'

    if debug:
        print_warnings(TEXT_DEBUG_ACTIVE)

    else:
        print_status(TEXT_CLEAR_CONTAINER)
        docker_clear_stage()


@task
def testme(debug=False):

    test_start()

    with settings(warn_only=True):
        video_file = 'VID_20180402_152729.mp4'

        test_command = 'docker exec {container_name} python  {test_script} -vid {video_file}'.format(
            container_name=TEST_IMAGE_NAME,
            test_script=test_setting.TEST_SCRIPT,
            video_file=video_file)
        # local('docker exec test_ubuntu_opencv python /workdir/source/VehicleCounting.py -vid /workdir/test/test_data/test.mp4')

        local(test_command)

    test_end(debug)


def sleep_with_reason(seconds, reason=''):
    print('sleep for {}, {} seconds'.format(reason, seconds,))
    time.sleep(seconds)
    print('sleep done')


@task
def run_unittest():
    debug = True
    # NOTE: the path that in the docker container
    DOCKER_WORK_DIR = '/workdir'
    UNITTEST_TESTSCRIPT = os.path.sep.join([DOCKER_WORK_DIR, 'test/test_main.py'])

    test_start()
    # sleep_with_reason(30, 'sleep for docker ready')

    test_command = 'python  {unittest_script}'.format(
        unittest_script=UNITTEST_TESTSCRIPT
    )
    docker_command = 'docker exec {container_name} {test_command}'.format(
        container_name=TEST_IMAGE_NAME,
        test_command=test_command
    )
    local('docker exec test_ubuntu_opencv python  /workdir/test/test_main.py')

    test_end(debug)
