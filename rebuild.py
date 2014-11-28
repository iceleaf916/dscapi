#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dscapi.settings")

from apps.statistics.models import UserInformation, InfoStatistics
from django.core.exceptions import ObjectDoesNotExist

def rebuild():
    all_infos = UserInformation.objects.all().order_by("last_date")
    current_date_info = None
    count = 0
    print all_infos.count()
    for info in all_infos:
        cur_date = info.last_date.date()
        if not current_date_info:
            current_date_info = InfoStatistics(date=cur_date, number=1)
        else:
            if current_date_info.date == cur_date:
                current_date_info.number += 1
            else:
                current_date_info.save()
                current_date_info = InfoStatistics(date=cur_date, number=1)
        count += 1
        print "\rProgress: %s" % count,
rebuild()
