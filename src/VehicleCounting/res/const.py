#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
import datetime

from pprint import pprint

import logging


CWD = os.path.dirname(os.path.abspath(__file__))
PROJ_HOME = os.path.sep.join([CWD, '..'])
sys.path.append(CWD)

DATE_FORMAT = '%d%m%YT%H%M%S'
LOG_PATH = os.path.sep.join([PROJ_HOME, '_log'])
LOG_FILENAME = datetime.datetime.now().strftime(DATE_FORMAT + '.log')
LOG_FULL_PATH = os.path.sep.join([LOG_PATH, LOG_FILENAME])


def init_logging():
    LOGGING_FORMATTER = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(LOGGING_FORMATTER)

    logging.basicConfig(
        level=logging.DEBUG,
        format=LOGGING_FORMATTER,
        datefmt='%d %m %Y %H:%M:%S',
        filename=LOG_FULL_PATH,
        filemode='a')

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use

    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    logging.debug('logging file save to {}'.format(LOG_FULL_PATH))
    # logging.debug('start')
    # logging.info('info')
    # logging.warning('warning')
    # logging.error('error')
    # logging.exception('exp')
    # logging.debug('end')
