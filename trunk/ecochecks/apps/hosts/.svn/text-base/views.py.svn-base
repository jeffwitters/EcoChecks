from django.shortcuts import render_to_response
from django.template.context import RequestContext

from models import Host

def hosts(request):
    hosts = Host.objects.all()
    return render_to_response('hosts/hosts.html', {
        'hosts': hosts,
    }, context_instance=RequestContext(request))
