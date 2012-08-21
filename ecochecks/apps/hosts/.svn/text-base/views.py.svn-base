from django.shortcuts import render_to_response
from django.template.context import RequestContext
from hosts.wiht_api import who_hosted_this
from hosts.forms import WhoishostingForm
from models import Host
from models import HostLookUp

def hosts(request):
    hosts = Host.objects.all()
    return render_to_response('hosts/hosts.html', {
        'hosts': hosts,
    }, context_instance=RequestContext(request))


def who_is_hosting(request):
    if request.method == 'POST':
        form = WhoishostingForm(request.POST)
        if form.is_valid():
            fdata =  form.cleaned_data
            domain = fdata['domain'];
            hosting_domain = who_hosted_this(domain)
            lookuptable = HostLookUp(domain = domain,hosted_by = hosting_domain)
            lookuptable.save()
            return render_to_response("hosts/who_hosted.html", {
                "hosted_by": hosting_domain,
            }, context_instance=RequestContext(request))
    else:
        form = WhoishostingForm()
    return render_to_response("hosts/whoishosting.html", {
        "form": form,
           }, context_instance=RequestContext(request))





def create_forum(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ForumCreateForm(request.POST) # A form bound to the POST data
        user_obj = request.user
        if user_obj is not None:
            user_obj = user_obj.id
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            fdata =  form.cleaned_data
            from datetime import date
            today = date.today()
            created_date = today
            modified_date = today

            data = {
                'forum_name':(fdata['forum_name']).strip(),
                'description':fdata['description'],
                'forum_type':(fdata['forum_type']).strip(),
                'forum_status':'OP',
                'forum_user':user_obj,
                'created_date':created_date,
                'modified_date':modified_date
                }

            if form :
                try:
                    forum_form = ForumCreateForm(data)
                    forum_form.save()
                except Exception:
                    print 'EXCEPTION'

            return HttpResponseRedirect('/forum/forum_list/') # Redirect after POST
    else:
        form = ForumCreateForm(initial = {'forum_status':'OP'}) # An unbound form
    return render_to_response('forumapp/forum_form.html', {'form': form},context_instance=RequestContext(request))


