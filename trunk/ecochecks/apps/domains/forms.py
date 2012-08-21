from django import forms
import re
import httplib
from httplib import HTTP
from urlparse import urlparse

from django.core.validators import URLValidator

class PainlessForm(forms.Form):
    name = forms.CharField(
        label=u'name:',
        max_length=30,
    )
    email = forms.EmailField(
        label=u'Email:'
    )
    phone_number = forms.IntegerField(
        required=False,
    )
    url = forms.URLField()
    current_host = forms.CharField(
        required=False,
    )
    message = forms.CharField(
        label='message:',
        widget=forms.Textarea(),
        max_length=300,
        required=False
    )

class CheckForm(forms.Form):
    domain = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"class":"domain"})
    )
    host = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"class":"host"})
    )

    def clean_domain(self):
        domain = self.cleaned_data['domain']
        is_ip = re.match("\d+\\.\d+\\.\d+\\.\d+", domain)
        dot_num = len(re.findall("\\.", domain))
        if dot_num < 1 or is_ip:
            raise forms.ValidationError('Invalid domain format!')
        else:
            domain_list = domain.split(".")
            if domain_list[-1] == domain_list[-2]:
                raise forms.ValidationError('Invalid domain url!')
            http_exist = len(re.findall("http://", domain))
            if http_exist >= 1:
                domain = domain[7:]
            www_exist = len(re.findall("www\\.", domain))
            if www_exist < 1:
                domain = "www."+domain
            try:
                conn = httplib.HTTPConnection(domain)
                conn.request("GET", '')
                r = conn.getresponse()
                if r.status != 200:
                    raise forms.ValidationError('Invalid domain url!')
                else:
                    return self.cleaned_data['domain']
            except:
                raise forms.ValidationError('Invalid domain url!')

    def clean_host(self):
        host = self.cleaned_data['host']
        dot_num = len(re.findall("\\.", host))
        if dot_num >= 1:
            http_exist = len(re.findall("http://", host))
            if http_exist >= 1:
                host = host[7:]
            www_exist = len(re.findall("www\\.", host))
            if www_exist < 1:
                host = "www."+host
            try:
                conn = httplib.HTTPConnection(host)
                conn.request("GET", '')
                r = conn.getresponse()
                if r.status != 200:
                    raise forms.ValidationError('Invalid host url!')
                else:
                    return self.cleaned_data['host']
            except:
                raise forms.ValidationError('Invalid host url!!')
        else:
            return self.cleaned_data['host']