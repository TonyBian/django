#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-08-24 16:05

"""get model fields"""

from setup_django import setup_django
from django.apps import apps

setup_django()


def get_model_fields(appname, modelname):
    modelobj = apps.get_model(appname, modelname)
    fieldlist = []
    for field in modelobj._meta.get_fields():
        fieldlist.append(str(field).split('.')[-1])

    fieldlist = [field for field in fieldlist if field[-1] != '>']
    return fieldlist
