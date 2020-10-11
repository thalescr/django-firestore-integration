from django.views.generic import TemplateView, FormView
from django.conf import settings
from core.generic import ListView, CreateView, DetailView, EditView, DetailView, DeleteView
from core.forms import LoginForm, RegisterForm, CertForm, SkillForm

# Home

class Home(TemplateView):
    template_name = 'core/home.html'

# Certs

class CertList(ListView):
    template_name = 'core/cert_list.html'
    collection = 'certs'

class CertCreate(CreateView):
    template_name = 'core/cert_form.html'
    form_class = CertForm
    collection = 'certs'

class CertEdit(EditView):
    template_name = 'core/cert_form.html'
    collection = 'certs'
    form_class = CertForm

class CertDelete(DeleteView):
    collection = 'certs'

# Skills

# Certs

class SkillList(ListView):
    template_name = 'core/skill_list.html'
    collection = 'skills'

class SkillCreate(CreateView):
    template_name = 'core/skill_form.html'
    form_class = SkillForm
    collection = 'skills'

class SkillEdit(EditView):
    template_name = 'core/skill_form.html'
    collection = 'skills'
    form_class = SkillForm

class SkillDelete(DeleteView):
    collection = 'skills'

# Authentication

import requests
from firebase_admin import auth

class Login(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword\
            ?key=' + settings.FIREBASE_WEB_API_TOKEN
        data = '{ "email" : {0}, "password" : {1}, "returnSecureToken" : true }'\
            .format(user['email'], user['password'])
        r = requests.post(url, data)
        if 'error' in r.json():
            return super().form_invalid(form)
        print(r.json())
        return super().form_valid(form)

class Register(FormView):
    template_name = 'core/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        auth.create_user(display_name=user['name'], email=user['email'],
            phone_number=user['phone'], photo_url=user['avatar'],
            password=user['password'])
        return super().form_valid(form)
        