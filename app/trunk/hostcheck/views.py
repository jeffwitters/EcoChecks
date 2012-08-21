import logging
import string
import pdb
import httplib
from datetime import date

import simplejson

from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import *
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required

# TODO Move
#from front.models import *
from hostcheck.forms import *
from hostcheck.models import *
from hostcheck.decorators import domain_approved 


def customize_domain(request, name):
    try:
        domain_name = DomainName.objects.get(name=name)
    except DomainName.DoesNotExist:
        request.flash['error'] = "Domain does not exist"
        return HttpResponseRedirect(reverse('index'))
        
    return render_to_response('front/profile/customize.html',
        context_instance=RequestContext(request, { 
            'domain_name' : domain_name 
            }))

def parse_domain_name(domain_name):
    """Parse the 'domain_name' into second-level domain and the rest.
    Care must be taken from TLDs and SLDs that are not part of the organization yet.
    For example: 
        
        "www.something.co.uk"
    
    The organization name would be something, but the function will return
    a tuple with the following elements:
        
        www.something.co.uk
        something.co.uk
        co.uk
        
    Unless we had a dictionary to remove "co.uk" we'll return it, unfortunately.
    So users of this function must handle these elements correctly.
    """
    
    tokens = domain_name.split(".")
    
    if len(tokens) > 2:
        elements = []
        
        for i, token in enumerate(tokens[:-1]):
            elements.append( ".".join(tokens[i:]))
    
        return elements 

    return [ domain_name ]

def company_approved(request, url):
    if url is None or len(url) == 0:
        request.flash['error'] = 'No company specified'
    
    try:
        company = HostingCompany.objects.get(url=url)
    except HostingCompany.DoesNotExist:
        request.flash['error'] = "Hosting company does not exist"

    if not company.checked:
        request.flash['error'] = "Company hasn't been checked"
        return HttpResponseRedirect(reverse('not-approved'))

    if not company.approved:
        request.flash['error'] = "Company is not carbon neutral"
        return HttpResponseRedirect(reverse('not-approved'))

    return render_to_response('hostcheck/company-approved.html',
        context_instance=RequestContext(request, { 'company' : company }))

# @domain_approved # TODO Blarg, can't get decorator right
def approved(request, name):
    if name is None or len(name) == 0:
        request.flash['error'] = 'Domain not specified'
        return HttpResponseRedirect(reverse('entity-not-found'))

    try:
        domain_name = DomainName.objects.get(name=name)
    except DomainName.DoesNotExist:
        request.flash['error'] = 'Domain name not found'
        return HttpResponseRedirect(reverse('entity-not-found'))

    company = domain_name.hosting_company
    if not company.approved:
        request.flash['error'] = 'Hosting company not approved'
        return HttpResponseRedirect(reverse('company-not-approved'))

    if not company.checked:
        request.flash['error'] = 'We haven\'t finished evaluating that company'
        return HttpResponseRedirect(reverse('company-not-approved'))

    return render_to_response('hostcheck/approved.html',
        context_instance=RequestContext(request, { 
            'company' : company, 'domain_name' : domain_name }))         

@login_required
def claim_domain_step_two(request, name=None):
    try:
        domain_name = DomainName.objects.get(name=name)
    except DomainName.DoesNotExist:
        request.flash['error'] = "No such domain name"
        return HttpResponseRedirect(reverse('profile')) 

    if domain_name.owner is not None:
        if domain_name.owner == request.user:   
            request.flash['error'] = "You are already owner of this domain"
        else:
            request.flash['error'] = "This domain is already claimed"
        
        return HttpResponseRedirect(reverse('profile'))

    domain_claim_token = None

    try:
        domain_claim_token = DomainClaimToken.objects.get(user=request.user, domain_name=domain_name)
    except DomainClaimToken.DoesNotExist:
        request.flash['error'] = "No claim token created"
        return HttpResponseRedirect(reverse('profile'))

    domain_check_url = "http://ecocheck%s/%s.html" % (domain_name.name, domain_claim_token.token) 
    
    conn = httplib.HTTPConnection(domain_name.name)
    conn.request("GET", "/ecocheck%s.html" % (domain_claim_token.token,)) 
    try:    
        resp = conn.getresponse()
        status = resp.status
        conn.close()

        if status == 200:
            # delete all tokens
            domain_name.owner = request.user
            domain_name.save()
                
            # Claim all tokens
            for token in DomainClaimToken.objects.filter(domain_name=domain_name):
                if domain_claim_token != token:                    
                    token.delete()
            
            domain_claim_token.claimed = True
            domain_claim_token.claimed_on = date.today()
            domain_claim_token.save()
            
            request.flash['message'] = "Thanks for claiming your domain"
            
            return render_to_response("hostcheck/claim_domain_name/success.html",
                context_instance=RequestContext(request, {
                    'domain_name' : domain_name }))
    except Exception, e:
        pass # TODO would be good to log this    
    request.flash['error'] = "The file doesn't seem to be on the server.  Please try again soon"
    
    return HttpResponseRedirect(reverse('claim-domain-name', kwargs={'name':domain_name.name}))

@login_required
def claim_domain(request, name=None):
    # TODO Modify so we perform this in a test
    try:
        domain_name = DomainName.objects.get(name=name)
    except DomainName.DoesNotExist:
        request.flash['error'] = "No such domain name"
        return HttpResponseRedirect(reverse('profile')) 

    if domain_name.owner is not None:
        if domain_name.owner == request.user:   
            request.flash['error'] = "You are already owner of this domain"
        else:
            request.flash['error'] = "This domain is already claimed"
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponseRedirect(reverse('index'))

    domain_claim_token = None

    try:
        domain_claim_token = DomainClaimToken.objects.get(user=request.user, domain_name=domain_name)
    except DomainClaimToken.DoesNotExist:
        # try to create it
        domain_claim_token = DomainClaimToken.objects.create(domain_name, request.user)

    return render_to_response('hostcheck/claim_domain_name/step2.html',
        context_instance=RequestContext(request, {
            'domain_name' : domain_name, 'token' : domain_claim_token }))

@login_required
def claim_domain_name_off(request, name=None):
    try:
        domain_name = DomainName.objects.get(name=name)
    except DomainName.DoesNotExist:
        request.flash['error'] = "No such domain name"
        return HttpResponseRedirect(reverse('profile')) 

    if domain_name.owner is not None:
        if domain_name.owner == request.user:   
            request.flash['error'] = "You are already owner of this domain"
        else:
            request.flash['error'] = "This domain is already claimed"
        
        return HttpResponseRedirect(reverse('profile'))

    return render_to_response('hostcheck/claim_domain_name/index.html',
        context_instance=RequestContext(request, 
            {'domain_name' : domain_name, 'hosting_company' : domain_name.hosting_company } )) 

def check_domain_name(request, name=None):
    """Show the certificate if the domain name was certified"""
    if name is None:
        raise Exception("Invalid domain name empty")

    name = name.strip()

    if len(name) == 0:
        #raise Exception("Invalid domain name, empty")
        request.flash['error'] = "No domain name specified"
        return HttpResponseRedirect(reverse('index'))

    try:
        domain_name = DomainName.objects.get(name=name)
    except DomainName.DoesNotExist:
        request.flash['error'] = "Domain name not found"
        return HttpResponseRedirect(reverse('index'))

    hosting_company = domain_name.hosting_company

    return render_to_response('hostcheck/approved.html',
        context_instance=RequestContext(request, {
            'domain_name' : domain_name, 
            'hosting_company' : hosting_company}))

def check(request):
    """Checks the host name or domain name or a domain.
    
    If the domain name is specified then it is checked and the hosting provider
    ignored.
    """
    
    if not request.is_ajax():
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == 'POST' or request.is_ajax():
        if request.is_ajax():
            form = CheckForm(request.GET)
        else:
            form = CheckForm(request.POST) 
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
                    
            domain_name = None
            company = None
 
            if 'url' in cleaned_data:
                url = cleaned_data['url']
                
                # parse out the plain second level domain and the sub-levels
                elements = parse_domain_name(url)                 
                domain_name = None
                
                for element in elements:
                    try:
                        domain_name = DomainName.objects.get(name=element)
                    except DomainName.DoesNotExist:
                        pass
            
                if not domain_name:            
                    request.flash['error'] = "Domain name not found"
                    if request.is_ajax():
                        return HttpResponse(simplejson.dumps({'error' : 'entity-not-found' }))
                        
                    return HttpResponseRedirect(reverse("entity-not-found"))

                company = domain_name.hosting_company   

            elif 'company_name_or_url' in cleaned_data:
                name_or_url = cleaned_data['company_name_or_url']
                company = None

                elements = parse_domain_name(name_or_url)

                for element in elements:
                    try:
                        company = HostingCompany.objects.get(url=element)
                    except HostingCompany.DoesNotExist:
                        pass
            
                if company is None:
                    try:
                        # Need to make case insensitive
                        company = HostingCompany.objects.get(name__icontains=name_or_url)
                    except HostingCompany.DoesNotExist:
                        pass
            

            if not company:
                request.flash['error'] = "Company not found"
                
                if request.is_ajax():                        
                    return HttpResponse(simplejson.dumps({'error' : 'entity-not-found' }))
                
                return HttpResponseRedirect(reverse('entity-not-found'))

            if not company.checked:
                if request.is_ajax():                        
                    return HttpResponse(simplejson.dumps({'error' :  'company-not-approved'}))
                
                request.flash['error'] = "Company hasn't been checked"                
                return HttpResponseRedirect(reverse('company-not-approved'))

            if not company.approved:
                if request.is_ajax():                        
                    return HttpResponse(simplejson.dumps({'error' :  'company-not-approved'}))

                request.flash['error'] = "Company is not carbon neutral!"
                return HttpResponseRedirect(reverse('company-not-approved'))

            # we're good.  send them to success
            if domain_name:
                if request.is_ajax():                        
                    if domain_name.owner is not None:
                        owner_id = domain_name.owner.id
                    else:
                        owner_id = None
                    
                    return HttpResponse(simplejson.dumps({'success' :  'approved',
                        'name' : domain_name.name,
                        'owner_id' : owner_id}))
                
                
                return HttpResponseRedirect(reverse('approved', kwargs={ 
                    'name' : domain_name.name,
                    
                     }))
            else:
                if request.is_ajax():                        
                    return HttpResponse(simplejson.dumps({'success' :  'approved'}))
                
                return HttpResponseRedirect(reverse('company-approved', kwargs={ 'url' : company.url} ))
        else:
            request.flash['error'] = "Please correct the errors below"

            if request.is_ajax():                        
                return HttpResponse(simplejson.dumps({'error' : "invalid-form",
                    'errors' : form.errors }))
            
    else:
        form = CheckForm()

    if request.is_ajax():                        
        return HttpResponseError("Nothing sent")
    
    return render_to_response('hostcheck/check.html',
                context_instance=RequestContext(request, { 'form' : form }))         



