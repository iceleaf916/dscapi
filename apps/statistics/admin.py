from django.contrib import admin
from apps.statistics.models import UserInformation

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'ip_address', 'last_date')
    date_hierarchy = 'last_date'

admin.site.register(UserInformation, UserInformationAdmin)
