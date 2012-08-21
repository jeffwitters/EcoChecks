from django.shortcuts import render_to_response,redirect
from django.template.context import RequestContext
from django.contrib.auth import logout,authenticate,login
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from account.forms import *

def main_page(request):
    return render_to_response("index.html", {
    }, context_instance=RequestContext(request))
    
def signupsuccess(request):
    return render_to_response("account/signup_success.html", {
                "success": '',
            }, context_instance=RequestContext(request))
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user = authenticate(username=username, password=password)
            login(request, user)
            send_mail(
                'EcoCheck Signup',
"Welcome to EcoChecks\n\n \
You're receiving this email because you registered \
your email address with the EcoChecks to validate a \
host or a domain name as being eco freindly and 100%% carbon neutral.\n\n\
Your Username:%s\n \
Your Password:%s\n\n \
Your Profile URL:http://www.ecochecks.com/domains/\n\n\n\n \
Thanks for joining!\n\n \
EcoChecks\n\n\n \
Follow us on Twitter(http://www.twitter.com/ecocheck) \
or Like Us on Facebook (http://www.facebook.com/pages/EcoChecks/107904242586494)\n\n\n \
This is an auto-generated email; please do not reply." % (form.cleaned_data['username'], 
                                                          form.cleaned_data['password']),
               
                'noreply@ecochecks.org',
                [form.cleaned_data['email']],
                fail_silently=True
            )
            
            return redirect('/account/signup_success/')
    else:
        form = SignupForm()
    variables = RequestContext(request, {'form':form})
    return render_to_response('account/signup.html', variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                next = request.GET.get("next", "")
                if next:
                    return redirect(next)
                return redirect('/domains/')
            else:
                form = LoginForm(request.POST)
                return render_to_response("account/login.html", {
                    "info": ['login failed'],
                    "form":form
                }, context_instance=RequestContext(request))
    else:
        form=LoginForm()
    return render_to_response("account/login.html", {
        "form":form
    }, context_instance=RequestContext(request))