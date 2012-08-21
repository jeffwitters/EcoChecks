from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^signup/$", "account.views.signup", name="signup"),
    url(r"^login/$", "account.views.login_page", name="login"),
    url(r"^logout/$", "account.views.logout_page", name="logout"),
    url(r"^signup_success/$", "account.views.signupsuccess", name="signup_success"),
    
    url(r"^password_reset/$", "django.contrib.auth.views.password_reset", 
        {"template_name":"account/password_reset_form.html", 
         "email_template_name":"account/password_reset_email.html"}, name="reset_password"),
    url(r"^password_reset/done/$", "django.contrib.auth.views.password_reset_done", 
        {"template_name":"account/password_reset_done.html"}, name="done_password"),
    url(r"^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", 
        "django.contrib.auth.views.password_reset_confirm", 
        {"template_name":"account/password_reset_confirm.html"}, name="confirm_password"),
    url(r"^reset/done/$", "django.contrib.auth.views.password_reset_complete", 
        {"template_name":"account/password_reset_complete.html"}, name="complete_password"),
)