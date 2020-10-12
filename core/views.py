from django.views.generic import TemplateView, FormView, RedirectView
from django.http import HttpResponseRedirect

from core import generic
from core.forms import LoginForm, RegisterForm, CertForm, SkillForm

# Home

class Home(generic.AuthenticatedMixin, TemplateView):   
    template_name = 'core/home.html'

# Certs

class CertList(generic.ListView):
    template_name = 'core/cert_list.html'
    collection = 'certs'

class CertCreate(generic.CreateView):
    template_name = 'core/cert_form.html'
    form_class = CertForm
    collection = 'certs'

class CertEdit(generic.EditView):
    template_name = 'core/cert_form.html'
    collection = 'certs'
    form_class = CertForm

class CertDelete(generic.DeleteView):
    collection = 'certs'

# Skills

class SkillList(generic.ListView):
    template_name = 'core/skill_list.html'
    collection = 'skills'

class SkillCreate(generic.CreateView):
    template_name = 'core/skill_form.html'
    form_class = SkillForm
    collection = 'skills'

class SkillEdit(generic.EditView):
    template_name = 'core/skill_form.html'
    collection = 'skills'
    form_class = SkillForm

class SkillDelete(generic.DeleteView):
    collection = 'skills'

# Authentication

import requests
from datetime import datetime, timedelta
from firebase_admin import auth
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore

class Login(generic.UnauthenticatedMixin, FormView):
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
        self.request.session.modified = True
        return super().form_valid(form)

class Logout(generic.AuthenticatedMixin, RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        """Clear session cookies"""
        try:
            del request.session['sessionid']
        except:
            pass
        return super().get(request, *args, **kwargs)

class Register(generic.UnauthenticatedMixin, FormView):
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
        