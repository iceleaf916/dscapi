from django.http import HttpResponse
from apps.statistics.models import UserInformation

def index(request):
    uid = request.GET.get('uid')
    if uid:
        remote_ip = request.META.get("REMOTE_ADDR")
        info = UserInformation(uuid=uid, ip_address=remote_ip)
        info.save()
        return HttpResponse("statistics %s" % uid)
    else:
        return HttpResponse("failed")
