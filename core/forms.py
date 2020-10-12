from datetime import datetime
from django import forms

# Authentication

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'joao.silva@email.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control white-text',
        'placeholder': '**********'
    }))

    def save(self):
        return self.cleaned_data

class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'João Silva'
    }))
    avatar = forms.FileField(required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'joao.silva@email.com'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control white-text',
        'placeholder': '(00) 00000-0000'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control white-text',
        'placeholder': '**********'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control white-text',
        'placeholder': '**********'
    }))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.data.get('password1')
        password2 = self.data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Senhas não coincidem!')
        return password2

    def save(self):
        user = self.cleaned_data
        del user['password2']
        user['password'] = self.clean_password2()
        ## Upload avatar file
        if user['avatar']:
            from firebase_admin import storage
            bucket = storage.bucket()
            new_avatar = bucket.blob('avatars/' + user['email'] + '/' + user['avatar'].name)
            new_avatar.upload_from_file(user['avatar'])
            new_avatar.make_public()
            user['avatar'] = new_avatar.public_url
        else:
            user['avatar'] = None
        print(user)
        return user

# Certs

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
        return data

# Skills

class SkillForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control white-text',
        'placeholder': 'Microsoft Word'
    }))
    skill_level = forms.IntegerField(widget=forms.Select(
        choices=(
            (1, 'Aprendiz'),
            (2, 'Básico'),
            (3, 'Intermediário'),
            (4, 'Avançado'),
            (5, 'Expert')
        )
    ))

    def save(self):
        return self.cleaned_data
