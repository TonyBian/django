#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-14 14:10

"""
"""

import sys
sys.path.append('../..')
from public.get_model_fields import get_model_fields


def get_fields_dict(
        model,
        exclude_fields_set,
        rawdata_dict,
        fields_dict):
    # get other field's name
    fields = get_model_fields('cmdb', model)
    other_fields = [
        field for field in fields
        if field not in (exclude_fields_set)
    ]
    # get other field's value and extend fields dict
    for field in other_fields:
        try:
            value = rawdata_dict[field]
        except KeyError:
            value = ''
        fields_dict.update({field: value})

    return fields_dict
