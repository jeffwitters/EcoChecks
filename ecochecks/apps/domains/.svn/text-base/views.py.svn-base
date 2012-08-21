from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from hosts.models import Host
import sys, uuid
import settings
import os
from domains.models import Domain, Log
from domains.forms import PainlessForm, CheckForm

import datetime
import urllib2
import urllib
import re
import httplib
import subprocess
from django.http import HttpResponse

@login_required
def domains(request):
    domains = Domain.objects.filter(user=request.user)
    return render_to_response("domains/domains.html", {
        "domains": domains,
    }, context_instance=RequestContext(request))
    
def index(request):
    return render_to_response("index.html", {
    }, context_instance=RequestContext(request))

def check(request):     
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            domain_url = form.cleaned_data['domain']
            hosting = form.cleaned_data['host']
            if domain_url != "Enter your Domain Name" and hosting != "Enter your web host":
                # the host is url or string
                dot_num = len(re.findall("\\.", hosting))
                if dot_num >= 1:
                    temp_host = hosting
                    if len(re.findall("http", hosting)) > 0:
                        temp_host = temp_host[8:]
                    if len(re.findall("www\\.", hosting)) > 0:
                        temp_host = temp_host[4:]
                    host = Host.objects.filter(signup_url__icontains=temp_host)
                else:
                    host = Host.objects.filter(name__icontains=hosting)
                # verify the host against certified green hosts
                if len(host) == 1:# green 
                    # save domain information
                    return redirect(reverse("before_verify")+"?domain="+domain_url+"&hostid="+str(host[0].id))
                elif len(host) > 1:# multiple host
                    host_errors="The host name is not accurate!"
                    return render_to_response("domains/check.html", {
                        "form":form,
                        "host_errors":host_errors
                    }, context_instance=RequestContext(request))
                else:# not find host
                    #here do IP ping
                    r = subprocess.Popen(['ping', domain_url, '-c 6'], stdout=subprocess.PIPE)
                    ip_text = r.stdout.read()
                    ipaddress = re.findall('\\((.+)\\):', ip_text)
                    hostname = re.findall('from (.+) \\(', ip_text)
                    ipstr = ''
                    server = ''
                    if len(ipaddress)>0:
                        ipstr = ipaddress[0]
                    else:
                        ipstr = 'not'
                    if len(hostname)>0:
                        server = hostname[0]
                    else:
                        server = 'not'
                    #here do whois
                    w = subprocess.Popen(['whois', domain_url], stdout=subprocess.PIPE)
                    whois_text = w.stdout.read()
                    logs = Log.objects.filter(url__icontains=domain_url)
                    if len(logs) >= 1:
                        log = logs[0]
                    else:
                        log = Log()
                    log.url = domain_url
                    log.host = hosting
                    log.ip = ipstr
                    log.server = server
                    log.whois = whois_text
                    log.save()
                    return redirect(reverse("co2_display", args=[log.id]))          
    else:
        form = CheckForm()
    return render_to_response("domains/check.html", {
            "form":form
    }, context_instance=RequestContext(request))

@login_required
def before_verify(request):
    host_id = request.GET["hostid"]
    domain_url = request.GET["domain"]
    #domain_url = "dev.ecochecks.org"
    host = get_object_or_404(Host, id=host_id)
    #domain = domain.replace(r"-", r".")
    if len(re.findall("www\\.", domain_url)) > 0:
        domains = Domain.objects.filter(url__icontains=domain_url[4:], user=request.user)
    else:
        domains = Domain.objects.filter(url__icontains=domain_url, user=request.user)
    if len(domains) > 0:
        domain = domains[0]
    else:
        domain = Domain()
    domain.user = request.user
    domain.url = domain_url
    domain.host = host
    domain.save()
    return redirect(reverse("verify_domain", args=[domain.id]))

@login_required
def verify(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    domain.user = request.user
    domain.save()
    error_info = ""
    if request.method == "POST":
        filename = request.POST['filename']
        conn = httplib.HTTPConnection(domain.url)
        conn.request("GET", "/"+filename)
        r = conn.getresponse()
        if r.status == 200:
            domain.verified = True
            domain.save()
            return redirect(reverse("customize_domain", args=[domain.id]))    
        else:
            error_info = "Verification failed, please try again!"
    return render_to_response("domains/verify.html", {
        "filename":str(uuid.uuid4())[0:18]+".html",
        "error_info":error_info,
        "domain":domain
    }, context_instance=RequestContext(request))

@login_required
def verify_meta(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    error_info = ""
    if request.method == "POST":
        metacontent = request.POST["metacontent"]
        url = "http://"
        url = url + domain.url
        u = urllib2.urlopen(url)
        buffer = u.read()
        is_find = re.findall(metacontent, buffer)
        if is_find:
            domain.verified = True
            domain.save()
            return redirect(reverse("customize_domain", args=[domain.id]))    
        else:
            error_info = "Verification failed, please try again!"
    return render_to_response("domains/verify_meta.html", {
        "metacontent": str(uuid.uuid4())[0:18].replace("-", "_"),
        "error_info": error_info,
        "domain": domain
    }, context_instance=RequestContext(request))
    
@login_required
def customize(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    # do ping.FM
    api_key = settings.API_KEY
    user_app_key = settings.USER_APP_KEY
    post_method = "default"
    body = "%s just EcoChecked %s and passed! " % (request.user.username, domain.url)
    url = 'http://api.ping.fm/v1/user.post'
    data = urllib.urlencode([('api_key',api_key),('user_app_key',user_app_key),
                             ('post_method',post_method),('body',body)])
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req, data)
    return render_to_response("domains/customize.html", {
        "domain": domain
    }, context_instance=RequestContext(request))

def upload_badge(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    if request.method == 'POST':
        try:
            file = request.FILES["Filedata"]
            badge_folder = "%s/badge" % settings.MEDIA_ROOT
            if not os.path.exists(badge_folder):
                os.makedirs(badge_folder)
            badge_file_name = "%s.png" % uuid.uuid4()
            destination = open("%s/%s" % (badge_folder, badge_file_name), 'wb')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            domain.badge_file_name = badge_file_name
            domain.awarded_date = datetime.datetime.now()
            domain.save()
        except:
            print sys.exc_info()[1]

    return redirect("/")

@login_required
def complete_badge(request, domain_id):
    domains = Domain.objects.filter(user=request.user)
    domain = get_object_or_404(Domain, id=domain_id)
    return render_to_response("domains/domains.html", {
        "host" : "http://"+request.META['HTTP_HOST'],
        "badge_file_name" : domain.badge_file_name,
        "domain" : domain,
        "domains": domains,
        "message":"Domain '%s' has been updated successfully" % domain

    }, context_instance=RequestContext(request))

@login_required
def offset_co2(request):
    return render_to_response("domains/offset.html", {
    }, context_instance=RequestContext(request))
    
def co2_display(request, log_id):
    log = get_object_or_404(Log, id=log_id)
    return render_to_response("domains/co2_display.html", {
        "log":log
    }, context_instance=RequestContext(request))
    
def not_approved(request):
    return render_to_response("domains/not_approved.html", {
    }, context_instance=RequestContext(request))
    
def painless_migrate(request):
    if request.method == 'POST':
        form = PainlessForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            url = form.cleaned_data['url']
            current_host = form.cleaned_data['current_host']
            message = form.cleaned_data['message']
            send_mail(
                'EcoCheck Painless Migration',
                'Name:%s \nEmail:%s \nPhoneNumber:%s \nURL:%s \nCurrentHos:%s \nMessage:\n%s' % (
                                            name, 
                                            email,
                                            phone_number,
                                            url,
                                            current_host,
                                            message,
                                            ),
                email,#from 
                [settings.CONTACT_MAIL],
                fail_silently=True
            )
            return render_to_response("contact/contact_success.html", {
                "name": name,
            }, context_instance=RequestContext(request))
    else:
        form = PainlessForm()
    return render_to_response("domains/painless_migration.html", {
        "form":form,
    }, context_instance=RequestContext(request))
    
def certified_hosts(request):
    hosts = Host.objects.all()
    return render_to_response("domains/certified_hosts.html", {
        "hosts": hosts,
    }, context_instance=RequestContext(request))

@login_required    
def modify_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)  
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            domain_url = form.cleaned_data['domain']
            hosting = form.cleaned_data['host']
            #host = Host.objects.get(name=hosting)
            if len(Host.objects.filter(name__icontains=hosting)) >= 1:
                host = Host.objects.get(name__icontains=hosting)
                domain.url = domain_url
                domain.host = host
                domain.save()
                return redirect('/domains/')
            else:
                host_errors = "Please input correct host name!"
                return render_to_response("domains/check.html", {
                    "form":form,
                    "host_errors":host_errors
                }, context_instance=RequestContext(request))
    else:
        form = CheckForm({"domain":domain.url, "host":domain.host.name})
    return render_to_response("domains/check.html", {
            "form":form
    }, context_instance=RequestContext(request))
    
@login_required
def delete_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    domain.delete()
    return redirect('/domains/')

@login_required
def certificate(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    return render_to_response("domains/certificate.html", {
            "domain":domain
    }, context_instance=RequestContext(request))
    
def process(request):
    #domains = Domain.objects.filter(user=request.user)
    return render_to_response("domains/process.html", {
    }, context_instance=RequestContext(request))
    
def download_html_file(request):
    file_name = request.GET["filename"]
    response = HttpResponse("", mimetype='text/html')
    response['Content-Disposition'] = 'attachment; filename='+file_name
    return response
