from django.conf.urls.defaults import *

from account.views import *
from domains.views import check

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ecochecks/', include('ecochecks.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', check),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r"^domains/", include("domains.urls")),
    (r"^hosts/", include("hosts.urls")),
    (r'^account/',include('account.urls')),
    (r'^contact/',include('contact.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^tinymce/', include('tinymce.urls')),
        #(r'^$', 'domains.views.check'),
    
    url(r'^comments/', include('django.contrib.comments.urls')),
    #url(r'^weblog/', include('zinnia.urls')),

    
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^weblog/', include('zinnia.urls')),

)
if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
            (r'^zinnia/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.ZINNIA_MEDIA_ROOT}),
        )
