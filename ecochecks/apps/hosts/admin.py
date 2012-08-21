from django.contrib import admin
from hosts.models import Host
from hosts.models import HostLookUp

admin.site.register(Host)
admin.site.register(HostLookUp)
