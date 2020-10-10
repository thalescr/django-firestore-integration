from datetime import datetime
from django import forms

class CertForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'Curso de datilografia'
    }))
    organization = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'Cursos Online'
    }))
    emission_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control white-text',
        'type': 'date'
    }))
    credential_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'AAAAA00000'
    }))
    credential_url = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'https://'
    }))

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', False)
        # Convert datetime if form has initial value
        if initial:
            initial['emission_date'] = initial['emission_date'].strftime('%Y-%m-%d')
            kwargs['initial'] = initial
        super(CertForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        ## Convert date to datetime
        data['emission_date'] = datetime.combine(self.cleaned_data['emission_date'],
            datetime.min.time())
        ## Add owner_id field
        data['owner_id'] = 1
        return data