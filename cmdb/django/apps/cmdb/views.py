# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# import sys
# from os import path
# sys.path.append('..')
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from django.http import HttpResponse


def all_grains(request):
    with open('/tmp/all_grains.txt', 'r') as grains_file:
        all_grains = grains_file.read()
    return HttpResponse(all_grains)
