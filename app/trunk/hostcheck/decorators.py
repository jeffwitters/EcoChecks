import pdb

try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper

from django.http import HttpResponseRedirect
from django.utils.http import urlquote

from hostcheck.models import *

def domain_approved(view_func):
    def decorate(view_func, name): 
        return _CheckDomain(view_func)

    return decorate


class _CheckDomain(object):
    def __init__(self, view_func):
        self.view_func = view_func
        update_wrapper(self, view_func)

    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _CheckDomain(view_func)
    
    def __call__(self, request, *args, **kwargs):

        pdb.set_trace()
        if not name:
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

        return self.view_func(request, *args, **kwargs)


