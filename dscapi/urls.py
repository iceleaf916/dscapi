from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import apps.statistics.urls

urlpatterns = patterns('',
    # Examples:
    url(r'^dscapi/$', 'dscapi.views.index'),
    url(r'^dscapi/statistics/', include(apps.statistics.urls)),

    # Uncomment the next line to enable the admin:
    url(r'^dscapi/admin/', include(admin.site.urls)),
)
