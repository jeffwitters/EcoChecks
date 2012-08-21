from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.mail import send_mail
from contact.forms import ContactForm
import settings

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                'EcoCheck SignUp',
                '%s \n    yours %s' % (message,name),
                email,
                [settings.CONTACT_MAIL],
                fail_silently=False
            )
            return render_to_response("contact/contact_success.html", {
                "name": name,
            }, context_instance=RequestContext(request))
    else:
        form = ContactForm()
    return render_to_response("contact/contactus.html", {
        "form": form,
    }, context_instance=RequestContext(request))