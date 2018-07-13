#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-21 15:06

""""""

import traceback
from django.utils import timezone


def get_exception(
        hostname,
        serialnumber,
        function,
        errtype,
        exception_model):
    try:
        function
    except errtype, e:
        errmsg = repr(e)
        tracebackmsg = traceback.format_exc()
        capture_date = timezone.now()

        exception = {
            'localhost': hostname,
            'SerialNumber': serialnumber,
            'errmsg': errmsg,
            'tracebackmsg': tracebackmsg,
            'capture_date': capture_date,
        }

    exception_model.objects.create(**exception)
