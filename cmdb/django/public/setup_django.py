#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-07 16:58

"""
 initial django
"""


def setup_django():
    import os
    import sys
    import django
    sys.path.append('..')
    from mysite.settings import BASE_DIR

    sys.path.append(BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()
