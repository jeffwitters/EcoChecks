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

    def __init__(self,*args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'nameStyle'
        self.fields['email'].widget.attrs['class'] = 'nameStyle'
        self.fields['message'].widget.attrs['class'] = 'messageStyle'
        self.fields['name'].widget.attrs['id'] = 'id_name'
        self.fields['email'].widget.attrs['id'] = 'id_email'
        self.fields['message'].widget.attrs['id'] = 'id_message'
