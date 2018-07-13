#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-18 17:39

""""""

from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(
        r'^all_grains/qHPVzFKCU3eHYWCXLMwTibxsnz9zRImn/$',
        views.all_grains,
        name='all_grains',
    )
]
