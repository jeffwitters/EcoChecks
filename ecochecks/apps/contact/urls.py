from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^$", "contact.views.contact_us", name="contact_us"),
    url(r"^../aboutus/", "/aboutus/", name="about_us"),
    url(r"^../faq/", "/faq/", name="faq_view"),
    url(r"^../privacypolicy/", "/privacypolicy/", name="privacy_policy"),
    url(r"^../termsofservice/", "/termsofservice/", name="terms_of_service"),
)
