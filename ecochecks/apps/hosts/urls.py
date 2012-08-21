from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'hosts.views.hosts', name='host_list'),
    url(r'^whoishosting$', 'hosts.views.who_is_hosting', name='who_is_hosting'),
)
