from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label=u'name:',
        max_length=30,
    )
    email = forms.EmailField(
        label=u'Email:'
    )
    message = forms.CharField(
        label='message:',
        widget=forms.Textarea(),
        max_length=300,
        required=False
    )