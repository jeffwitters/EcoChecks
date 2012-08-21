import logging
import string
import pdb
from datetime import datetime

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import *
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from front.models import *
from front.forms import *
from front.util import *

from django import forms
class UploadBadgeForm(forms.Form):
    Filedata = forms.FileField()

def upload_badge(request):
    """Temporary test for uploading image files"""
    try:
        if request.method == 'POST':
            #print request.FILES
            form = UploadBadgeForm(request.POST, request.FILES)

            if form.is_valid():
                #hadle_uploaded_file(request,FILES['file'])
                f = request.FILES['Filedata']
                #print settings.BADGE_UPLOAD_PATH
                filename = os.path.join(settings.BADGE_UPLOAD_PATH, 
                f.name)
                
                #print "writing to", filename
                
                destination = open(filename, 'wb+')

                for chunk in f.chunks():
                    destination.write(chunk)
                    destination.close()

                    return HttpResponse('Worked!')
            #print "didn't work"
            return HttpResponse('Didn\'t work')
        #print "was not a post"
        return HttpResponse("Wasn't a post!")
    except Exception, e:
        #import traceback
        #traceback.print_exc()
        raise e

def rss_feed(request):
    return HttpResponse("NOM NOM NOM")

# Profile related views
def profile_signup(request):

    if request.method == 'POST':
        form = ProfileSignupForm(request.POST)
            
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # create a signup request token
            user = User(username=cleaned_data['username'],
                    email=cleaned_data['email'], is_active=False)              
            user.set_password(cleaned_data['password'])
            user.save()

            registration_token = RegistrationToken.objects.create_token(user)
            
            # send email out 
            send_registration_token_email(user, registration_token)             
            request.flash['message'] = "Your activation link has been sent to the email you provided"

            return HttpResponseRedirect(reverse("profile-activate-empty")) 
        else:
            request.flash['error'] = "Please correct the errors below"
    
    else:
        form = ProfileSignupForm()    

    return render_to_response('front/profile/signup.html',
        context_instance=RequestContext(request, {
            'form' : form })) 

def about(request):
    request.here_now = 'about'
    return render_to_response('front/about.html', 
        context_instance=RequestContext(request))

def process(request):
    request.here_now='process'
    return render_to_response('front/process.html',
        context_instance=RequestContext(request))
        
def certified_hosts(request):
    request.here_now='certified-hosts'
    

    return render_to_response('front/certified_hosts.html',
        context_instance=RequestContext(request))

def contact(request):
    request.here_now='contact'
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['sender_ip'] = request.META['REMOTE_ADDR']
            # TODO Maybe we'll put this in a db because it takes to long to send email
            #send_mail('Ecochecks: Feedback from contact form',
            #   cleaned_data['message'], 
            #   "%s <%s>" % (cleaned_data['name'], cleaned_data['email']),
            #   [ settings.FEEDBACK_EMAIL ])
            try:
                feedback = Feedback(**cleaned_data)
                feedback.save()
            
                request.flash['message'] = "Thank you for your feedback"
                return HttpResponseRedirect(reverse('index'))
            except Exception, e:
                # log it
                # need to setup exception logging
                logging.exception(e)
                request.flash['error'] = "Unable to send your feedback.  Please try again in a few minutes"
                
                
        else:
            request.flash['error'] = "Please correct the errors below"
        
    else:
        form = ContactForm()
    
    
    return render_to_response('front/contact.html',
        context_instance=RequestContext(request, { 'form' : form }))



def profile_activate(request, code=None):
    if code is not None or request.method == 'POST':
        
        if request.method == 'POST':
            data = request.POST
        elif code is not None:
            data = { 'code' : code }
            
        form = ProfileActivateForm(data)

        if form.is_valid():
            request.flash['message'] = "Was valid"
            token = form.get_token()

            user = token.user
            user.is_active = True
            token.delete()
            user.save()

            request.flash['message'] = "Your account has been activated, please login"

            return HttpResponseRedirect(settings.LOGIN_URL)                
        else: 
            request.flash['error'] = "Please correct the errors below"

    else:
        form = ProfileActivateForm()

    return render_to_response('front/profile/activate.html',
        context_instance=RequestContext(request, {
            'form' : form })) 

def profile_checkdomain(request):
    if 'domain_name' in request.POST:
        domain_name = request.POST.get('domain_name')

        return HttpResponseRedirect(reverse('check-domain-name', 
            kwargs={'name':domain_name}))  

@login_required
def profile(request):
    domain_names = request.user.domain_names.all()

    return render_to_response('front/profile/index.html',
        context_instance=RequestContext(request, {
            'domain_names' : domain_names })) 

            
def index(request):
    # get latest new items
    news_items = NewsItem.objects.filter(published=True)[:4]
    
    news_item = None

    if len(news_items) > 0:
        news_item = news_items[0]
    
    return render_to_response('front/index.html',
        context_instance=RequestContext(request, {
            'news_items' : news_items, 'news_item' : news_item
        }))

def request_badge(request):
    """Serves the badge.  
    Checks the referrer.  If the referrer is
    not in the list of approved domain names then
    it will add a warning badge to the tag.  Otherwise, it
    serves the badge"""
    pass
            
def newsletter_signup(request):
    """Takes a request with an email and signs the user up.  The user is sent a
    signup confirmation email to prevent spam.
    
    """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            subscription = None
            # Find out if there's an email like that
            try:
                subscription = NewsletterSubscription.objects.get(email=email)
            except NewsletterSubscription.DoesNotExist:
                pass
                
            # We'll let the user think that it worked just so people cannot spam
            if not subscription:
                subscription = NewsletterSubscription(email=email)
                subscription.save()
                
                newsletter_request = NewsletterSignupRequest.objects.create_request( 
                    subscription, request.META['REMOTE_ADDR'])
                
                # email the request    
                send_subscription_confirmation_email(subscription, newsletter_request)
                newsletter_request.sent_on = datetime.now()
                newsletter_request.save()
                
            request.flash['message'] = "Thanks for signing up"
            return HttpResponseRedirect(reverse('index'))    
        else:
            request.flash['error'] = "Please correct the errors below"
    else:
        form = NewsletterSignupForm()
    
    return render_to_response('front/newsletter/index.html',
        context_instance=RequestContext(request, { 'form' : form })
        )

def newsletter_activate(request, code=None):
    if request.method == 'POST' or code is not None:
        if code is not None:
            data = { 'code' : code }
        else:
            data = request.POST
            
        form = NewsletterActivationForm(data)
        
        if form.is_valid():
            code = form.cleaned_data['code']
                
            try:
                subscription_request = NewsletterSignupRequest.objects.get(code=code)
            except NewsletterSignupRequest.DoesNotExist:
                request.flash['error'] = "The code doesn't match any newsletter subscription request"
            else:
                subscription = subscription_request.newsletter_subscription
                subscription.activated = True
                subscription.activated_on = datetime.now()
                subscription.save()
                
                subscription_request.delete()
                
                request.flash['message'] = "Thank you.  Your subscription has been confirmed"
                
                return HttpResponseRedirect(reverse('index'))
        else:
            request.flash['error'] = "Please correct the errors below"
    else:
        form = NewsletterActivationForm()
    
    return render_to_response('front/newsletter/activate.html',
        context_instance=RequestContext(request, { 'form' : form }))

def newsletter_unsubscribe(requests):
    """Unsubscribe user from list."""
    pass
