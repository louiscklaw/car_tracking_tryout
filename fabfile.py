#!/usr/bin/env python

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

DOCKER_DIR = './docker'

docker_settings = {
    'DOCKER_DIR': DOCKER_DIR
}

TEST_IMAGE_NAME = 'test_ubuntu_opencv'


from fabric.colors import *


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
        local('docker kill $(docker ps -q -a)')
        local('docker rm $(docker ps -q -a)')


@task
def up():
    docker_clear_stage()

    with settings(warn_only=True):
        local('docker kill {}'.format(TEST_IMAGE_NAME))
        local('docker rm {}'.format(TEST_IMAGE_NAME))
    local('docker create --name {} -p 5901:5901 logickee/ubuntu_opencv'.format(TEST_IMAGE_NAME))

    local('docker start   {}  '.format(TEST_IMAGE_NAME))


@task
def testme(debug=False):
    TEXT_DEBUG_ACTIVE = 'debug active, ignore delete docker'
    TEXT_CLEAR_CONTAINER = 'cleaning container'
    up()
    sync_proj_files()
    with settings(warn_only=True):
        local('docker exec test_ubuntu_opencv python /workdir/source/VehicleCounting/VehicleCounting.py -vid /workdir/test/test_data/test.mp4')

    if debug:
        print_warnings(TEXT_DEBUG_ACTIVE)

    else:
        print_status(TEXT_CLEAR_CONTAINER)
        docker_clear_stage()
