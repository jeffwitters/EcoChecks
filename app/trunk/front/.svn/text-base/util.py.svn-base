from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.mail import *
from django.template.loader import render_to_string

def send_registration_token_email(user, registration_token):
    """Send a registration email to the user above"""
    activation_url = "http://%s%s" % (Site.objects.get_current().domain,
        reverse('profile-activate', kwargs={'code':registration_token.code}))

    data = {    'user' : user, 
                'registration_token' : registration_token,
                'activation_url' : activation_url } 
    
    html_content = render_template('email/activate.html', data)
    text_content = render_template('email/activate.txt', data)

    send_message("Ecochecks.org Activation Code", 
        settings.DEFAULT_SENDER_EMAIL, user.email, text_content, html_content)

def render_template(template_name, data):
    return render_to_string(template_name, data)

def send_message(subject, sender, recipient, text_content, html_content=None):
    msg = EmailMultiAlternatives(subject, html_content, sender, [recipient])
    msg.content_subtype = "html"
    msg.attach_alternative(text_content, "text/plain")

    msg.send()

def send_subscription_confirmation_email(subscription, request):
    activation_page_url = "http://%s%s" % (Site.objects.get_current().domain,
        reverse('newsletter-activate-empty'))
    activation_url =     "http://%s%s" % (Site.objects.get_current().domain,
        reverse('newsletter-activate', kwargs={'code':request.code}))
        
    data = { 'email' : subscription.email, 
        'request' : request, 
        'activation_url' : activation_url,
        'activation_page_url' : activation_page_url }
    
    html_content = render_template('email/newsletter/confirmation.html', data)
    text_content = render_template('email/newsletter/confirmation.txt', data)
    
    send_message("Ecochecks.org Newsletter Subscription Confirmation", 
           settings.DEFAULT_SENDER_EMAIL, subscription.email, 
           text_content, html_content)