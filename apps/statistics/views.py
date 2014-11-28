#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2014 Deepin, Inc.
#               2013~2014 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from apps.statistics.models import UserInformation, InfoStatistics
from apps.statistics.ip_search import IpLocater, string2ip

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

import os

def index(request):
    uid = request.GET.get('uid')
    if uid:
        remote_ip = request.META.get("REMOTE_ADDR")
        info = UserInformation(uuid=uid, ip_address=remote_ip)
        info.save()
        cur_date = info.last_date.date()
        try:
            info_statistics = InfoStatistics.objects.get(date=cur_date)
            info_statistics.number += 1
        except ObjectDoesNotExist:
            info_statistics = InfoStatistics(date=cur_date, number=1)
        info_statistics.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("failed")

def show_today(request):
    all_info = UserInformation.objects.all().order_by("-last_date")
    ip_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "qqwry.dat")
    ip_locater = IpLocater(ip_data_path)
    results = {}
    users = []
    start_date = "2014-01-06"
    for item in all_info:
        if item.uuid not in users:
            users.append(item.uuid)
            address = ip_locater.getIpAddr(string2ip(item.ip_address)).decode("GBK").encode("utf-8")
            if not results.get(address):
                results[address] = 1
            else:
                results[address] += 1

    new_infos = [(key, results[key]) for key in results]
    number = len(new_infos)
    for i in xrange(number-1):
        for j in xrange(number-i-1):
            if (new_infos[j][1] < new_infos[j+1][1]):
                new_infos[j], new_infos[j+1] = new_infos[j+1], new_infos[j]
    #if len(new_infos) > 30:
        #new_infos = new_infos[:30]
    return_str = "<h4>从%s至今，总的用户量为：%s</h4><p>" % (start_date, len(users))
    for (s, n) in new_infos:
        return_str += "%s: %s<br />" % (s, n)
    return_str += "</p>"
    return HttpResponse(return_str)

def show_chart(request):
    all_infos = InfoStatistics.objects.all().order_by("date")
    data = []
    for info in all_infos:
        last_date = info.date
        key = last_date.strftime("%Y-%m-%d")
        data.append(dict(date=key, value=info.number))

    return render_to_response(
        'result_chart.html',
        {"data": data},
        context_instance=RequestContext(request))
