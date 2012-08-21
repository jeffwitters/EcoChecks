from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

from front.models import *

class ContactForm(forms.Form):
	name = forms.CharField(max_length=30)
	email = forms.EmailField()
	message = forms.CharField(max_length=500, widget=forms.Textarea)

class ProfileSignupForm(forms.Form):
    #first_name = forms.CharField(max_length=30)
    #last_name = forms.CharField(max_length=30)
    username = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password_again =forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username']
        
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError(_("Please try another username"))
        except User.DoesNotExist:
            pass        

        return username 

    def clean(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password != password_again:
            raise forms.ValidationError(_("The passwords must match"))
        
        return self.cleaned_data

class SignonForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.user_cache = None
        super(SignonForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user_cache = authenticate(username=username, password=password)
        
        if self.user_cache is None:
            raise forms.ValidationError(_("Please enter a correct username and password"))
        elif not self.user_cache.is_active:
            raise forms.ValidationError(_("This account is inactive"))

    def get_user(self):
        return self.user_cache

class SignupForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()

class ProfileActivateForm(forms.Form):
    code = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        self.cached_token = None
        super(ProfileActivateForm, self).__init__(*args, **kwargs)    

    def clean_code(self):
        code = self.cleaned_data.get('code')
        
        try:
            self.cached_token = RegistrationToken.objects.get(code=code)
        except RegistrationToken.DoesNotExist:
            raise forms.ValidationError(_("Invalid activation code"))
        
        delta = date.today(), self.cached_token.created_on.date()

        if (date.today() - self.cached_token.created_on.date()).days > settings.MAX_REGISTRATION_TOKEN_DAYS:
            self.cached_token.user.delete()
            self.cached_token.delete()
            raise forms.ValidationError(_("Token is too old")) 

        return code 
    
    def get_token(self):
        return self.cached_token


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField()

class NewsletterActivationForm(forms.Form):
    code = forms.CharField(max_length=50)
    
    
