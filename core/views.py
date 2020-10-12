from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from core.generic import ListView, CreateView, DetailView, EditView, DetailView, DeleteView
from core.forms import LoginForm, RegisterForm, CertForm, SkillForm
from core.decorators import authenticated, not_authenticated

# Home

@method_decorator(authenticated, name='dispatch')
class Home(TemplateView):   
    template_name = 'core/home.html'

# Certs

@method_decorator(authenticated, name='dispatch')
class CertList(ListView):
    template_name = 'core/cert_list.html'
    collection = 'certs'

@method_decorator(authenticated, name='dispatch')
class CertCreate(CreateView):
    template_name = 'core/cert_form.html'
    form_class = CertForm
    collection = 'certs'

@method_decorator(authenticated, name='dispatch')
class CertEdit(EditView):
    template_name = 'core/cert_form.html'
    collection = 'certs'
    form_class = CertForm

@method_decorator(authenticated, name='dispatch')
class CertDelete(DeleteView):
    collection = 'certs'

# Skills

@method_decorator(authenticated, name='dispatch')
class SkillList(ListView):
    template_name = 'core/skill_list.html'
    collection = 'skills'

@method_decorator(authenticated, name='dispatch')
class SkillCreate(CreateView):
    template_name = 'core/skill_form.html'
    form_class = SkillForm
    collection = 'skills'

@method_decorator(authenticated, name='dispatch')
class SkillEdit(EditView):
    template_name = 'core/skill_form.html'
    collection = 'skills'
    form_class = SkillForm

@method_decorator(authenticated, name='dispatch')
class SkillDelete(DeleteView):
    collection = 'skills'

# Authentication

import requests
from datetime import datetime, timedelta
from firebase_admin import auth
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore

@method_decorator(not_authenticated, name='dispatch')
class Login(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key='\
            + settings.FIREBASE_WEB_API_TOKEN
        data = '{ "email" : "' + user['email'] +'", "password" : "'\
            + user['password'] + '", "useSecureToken" : true }'
        r = requests.post(url, data).json()
        errors = r.get('error', False)
        if errors:
            return HttpResponseRedirect(self.request.path + '?error=Login ou senha inválidos')
        self.request.session['sessionid'] = r.get('idToken')
        self.request.session['userid'] = r.get('localId')
        self.request.session.modified = True
        return super().form_valid(form)

@method_decorator(not_authenticated, name='dispatch')
class Register(FormView):
    template_name = 'core/register.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        user = form.save()
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key='\
            + settings.FIREBASE_WEB_API_TOKEN
        data = '{ "email" : "' + user['email'] + '", "password" : "'\
            + user['password'] + '", "useSecureToken": true }'
        r = requests.post(url, data)
        errors = r.json().get('error', False)
        if errors:
            return HttpResponseRedirect(self.request.path\
                + '?error=Cadastro inválido! Tente novamente.')
        auth.update_user(r.json().get('localId'), display_name=user['name'],
            phone_number=user['phone'], photo_url=user['avatar'], email_verified=True)
        return super().form_valid(form)
        