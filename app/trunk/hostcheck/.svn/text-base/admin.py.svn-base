from django.contrib import admin
from hostcheck.models import *


class HostingCompanyAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'url', 'checked', 'approved', 'created_on', 'checked_on']

admin.site.register(HostingCompany, HostingCompanyAdmin)

class DomainNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on']

admin.site.register(DomainName, DomainNameAdmin)

class DomainClaimTokenAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'user', 'token', 'claimed', 'created_on', 'claimed_on']

admin.site.register(DomainClaimToken, DomainClaimTokenAdmin)



