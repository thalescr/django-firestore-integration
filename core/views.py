from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.conf import settings
from core.generic import ListView, CreateView, DetailView, EditView, DetailView
from core.forms import CertForm

# Certs

class CertList(ListView):
    template_name = 'core/cert_list.html'
    collection = 'certs'

class CertCreate(CreateView):
    template_name = 'core/cert_form.html'
    form_class = CertForm
    collection = 'certs'

class CertDetail(DetailView):
    template_name = 'core/cert_detail.html'
    collection = 'certs'

class CertEdit(EditView):
    template_name = 'core/cert_form.html'
    collection = 'certs'
    form_class = CertForm

# Skills

# Authentication

class Login(TemplateView):
    template_name = 'core/login.html'

class Register(TemplateView):
    template_name = 'core/register.html'