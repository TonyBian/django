#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2018-01-16 17:21
# Filename      : __init__.py

"""
 initial scripts
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from mysite.settings import APPS_DIR
sys.path.insert(0, APPS_DIR)
