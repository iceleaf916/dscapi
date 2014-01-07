from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.statistics.views',
    url(r'^$', 'index'),
    url(r'^location/$', 'location'),
)
