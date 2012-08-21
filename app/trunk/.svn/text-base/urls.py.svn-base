from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
 
from django.contrib import admin
admin.autodiscover()

#url(r'^(?:index\.)?(?:php|html)?$', 'front.views.signup', 
#        name='index'),

urlpatterns = patterns('',
    
    url(r'^hidden-index/$', 'front.views.index', name='index'),

    # simple pages that don't change much if at all
    url(r'^about/$', 'front.views.about', name='about'),
    url(r'^process/$', 'front.views.process', name='process'),
    url(r'^certified-hosts/$', 'front.views.certified_hosts', 
        name='certified-hosts'),
    url(r'^contact/$', 'front.views.contact', 
            name='contact'),
    url(r'^feeds/$', 'front.views.rss_feed', name='rss-feed'),
            
    # process pages     
    url(r'^check/$', 'hostcheck.views.check', name='check'),
            
    # None ajax
    url(r'^not-found/', 'django.views.generic.simple.direct_to_template',
            { 'template' : 'hostcheck/entity-not-found.html' }, 
            name='entity-not-found' ),
    url(r'^not-approved/', 'django.views.generic.simple.direct_to_template',
            { 'template' : 'hostcheck/company-not-approved.html' }, 
            name='company-not-approved' ),
    url(r'^approved/(?P<name>[A-Za-z0-9\-\_\.]+)/$', 
            'hostcheck.views.approved', 
            name='approved'),
    url(r'^company-approved/(?P<url>[A-Za-z0-9\-\_\.]+)/$', 
            'hostcheck.views.company_approved', 
            name='company-approved'),
    
    ################################################
    # NEWSLETTER
    url(r'^newsletter/$', 
            'front.views.newsletter_signup', 
            name='newsletter'),
   
    url(r'^newsletter/confirm/(?P<code>[A-Za-z0-9\-\_\.]+)/?',
               'front.views.newsletter_activate', 
               name='newsletter-activate'),

    url(r'^newsletter/confirm/?',
            'front.views.newsletter_activate', 
            name='newsletter-activate-empty'),
            
   


    # UPLOADS
    url(r'^uploads_badge/', 'front.views.upload_badge', name='upload-badge'),

    # Domain name check 
    url(r'^domain/(?P<name>[A-Za-z0-9\-\_\.]*)/?$', 
            'hostcheck.views.check_domain_name', name='check-domain-name'),
    #url(r'^domain/(?P<name>[A-Za-z0-9\-\_\.]+)/claim/$',
    #        'hostcheck.views.claim_domain_name', name='claim-domain-name'),
    url(r'^domain/(?P<name>[A-Za-z0-9\-\_\.]+)/claim/$',
            'hostcheck.views.claim_domain', name='claim-domain-name'),
    url(r'^domain/(?P<name>[A-Za-z0-9\-\_\.]+)/claim/step2/$',
            'hostcheck.views.claim_domain_step_two', name='claim-domain-step-two'),
    url(r'^domain/(?P<name>[A-Za-z0-9\-\_\.]+)/customize/$',
            'hostcheck.views.customize_domain', name='customize-domain'),
    # profile stuff
    url(r'^signup2/$', 'front.views.profile_signup', name='signup2'),
    
    url(r'^signon/$', 'django.contrib.auth.views.login', kwargs={ 
        'template_name' : 'front/profile/signon.html'}, name='signon') ,
        
        
    url(r'^signoff/$', 'django.contrib.auth.views.logout', kwargs={
        'next_page' : '/hidden-index/' }, name='signoff'),
    url(r'^profile/$', 'front.views.profile', name='profile'),
    url(r'^profile/activate/$',
            'front.views.profile_activate', name='profile-activate-empty'),
    url(r'^profile/activate/(?P<code>[A-Za-z0-9\-\_\.]+)/?$', 
            'front.views.profile_activate', name='profile-activate'),
    url(r'^profile/check_domain', 
            'front.views.profile_checkdomain', name='forward-check-domain'),

    url(r'^thanks/$', 'django.views.generic.simple.direct_to_template',
        { 'template' : 'front/signup_thanks.html' }, name='signup-thanks'),
    url(r'^signup/$', 'front.views.profile_signup', name='signup'),
    
    # Admin stuff here
    (r'^admin/(.*)', admin.site.root),
)
