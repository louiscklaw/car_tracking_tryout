#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
import datetime

from pprint import pprint


class STATUS():
    OPENING_VIDEO = 'opening video '
    GETTING_PROPERTIES_FROM_SOURCE = 'getting properties from video source'


class ERRORS():
    OPEN_VIDEO_SOURCE = 'error opening video source'
    GETTING_PROPERTIES_FROM_SOURCE = 'error during getting properties from video source'
