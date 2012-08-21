import re
from django import forms
from django.contrib.auth.models import User
from django.core.validators import email_re

class SignupForm(forms.Form):
    username = forms.CharField(
        label = u'user name:',
        max_length = 30,
    )
    email = forms.EmailField(
        label = u'Email:',
        initial = "Your Email Address",
    )
    password=forms.CharField(
        label = u'Password:',
        widget = forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError('You input the invalid characters!')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('The username has been used!')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email_re.match(email):
            raise forms.ValidationError('Email address is not invalid!')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('The email has been registered!')
 
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())