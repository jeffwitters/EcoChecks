import pdb

from django import forms

class CheckForm(forms.Form):

    url = forms.CharField(max_length=250, required=False)
    company_name_or_url = forms.CharField(max_length=250, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data

        required_keys = ('url', 'company_name_or_url')
        
        for key in required_keys:
            if key in cleaned_data:
                value = cleaned_data[key].strip()
                if len(value) == 0:
                    del cleaned_data[key]
            
        if not 'url' in cleaned_data and not 'company_name_or_url' in cleaned_data:
            raise forms.ValidationError("You must specify at least one of the fields")

        return cleaned_data


