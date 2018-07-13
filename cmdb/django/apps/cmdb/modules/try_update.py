#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-14 13:38

"""
try to update database, and insert history into the change history table
"""

from __future__ import unicode_literals
import django
from django.utils import timezone


def try_update(
        serialnumber,
        model,
        chg_his_model,
        fields_dict,
        filter_dict,
        offlog_fields_set=set()):
    try:
        model.objects.create(**fields_dict)
    except django.db.utils.IntegrityError:
        queryset = model.objects.filter(**filter_dict)
        fields_dict_history = list(queryset.values())[0]

        fields_dict_temp = fields_dict
        for field in offlog_fields_set:
            try:
                fields_dict_temp.pop(field)
            except KeyError:
                continue

        change_count = 0
        for field in fields_dict_temp.iterkeys():
            if fields_dict_temp[field] != fields_dict_history[field]:
                change_history = {
                    'SerialNumber_id': serialnumber,
                    'model_name': model,
                    'field_name': field,
                    'old_value': fields_dict_history[field],
                    'new_value': fields_dict[field],
                    'change_date': unicode(timezone.now()),
                }
                chg_his_model.objects.create(**change_history)
                change_count += 1

        if change_count >= 1:
            queryset.update(**fields_dict)
