from django.http import HttpResponse
from apps.statistics.models import UserInformation
from apps.statistics.ip_search import IpLocater, string2ip

import os

def index(request):
    uid = request.GET.get('uid')
    if uid:
        remote_ip = request.META.get("REMOTE_ADDR")
        info = UserInformation(uuid=uid, ip_address=remote_ip)
        info.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("failed")

def location(request):
    date = request.GET.get('date')
    all_info = UserInformation.objects.all()
    ip_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "qqwry.dat")
    ip_locater = IpLocater(ip_data_path)
    results = {}
    for item in all_info:
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
    if len(new_infos) > 30:
        new_infos = new_infos[:30]
    return_str = "<p>"
    for (s, n) in new_infos:
        return_str += "%s: %s<br />" % (s, n)
    return_str += "</p>"
    return HttpResponse(return_str)
