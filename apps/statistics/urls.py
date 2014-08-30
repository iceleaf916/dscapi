from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.statistics.views',
    url(r'^$', 'index'),
    url(r'^today/$', 'show_today'),
    url(r'^chart/$', 'show_chart'),
)
