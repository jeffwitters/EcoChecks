from django import forms
from hosts.models import *
from hosts.wiht_api import who_hosted_this

class WhoishostingForm(forms.ModelForm):
   class Meta:
       model = HostLookUp
       fields = ['domain']
   def __init__(self,*args, **kwargs):
       super(WhoishostingForm, self).__init__(*args, **kwargs)
       self.fields['domain'].widget.attrs['class'] = 'nameStyle'
   def clean_domain(self):
       domain = (self.cleaned_data['domain']).strip()
       hosting_domain = who_hosted_this(domain)
       print hosting_domain
       if hosting_domain == None:
           raise forms.ValidationError("Invalid Domain!")
       return domain