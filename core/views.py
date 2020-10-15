from django.views.generic import TemplateView, FormView, RedirectView
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from firebase_admin import auth

from core import generic
from core.forms import LoginForm, RegisterForm, CertForm, SkillForm

db = settings.FIRESTORE_CLIENT

# Home

class Home(generic.AuthenticatedMixin, TemplateView):   
    template_name = 'core/home.html'

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('search', None)
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.query:
            return ['core/search.html']
        return super().get_template_names()

    def get_results(self):
        result = list()
        for user in auth.list_users().users:
            data = user._data.get('providerUserInfo')[-1]
            data['id'] = user._data.get('localId')
            if self.query in str(data.get('displayName')) or\
                self.query in str(data.get('email')):
                result.append(data)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.query:
            context['results'] = self.get_results()
            context['query'] = self.query
        return context

class UserView(generic.AuthenticatedMixin, TemplateView):
    template_name = 'core/user.html'
    def get(self, request, id, *args, **kwargs):
        if id:
            self.query_user = auth.get_user(id)._data
            if self.query_user:
                return super().get(request, *args, **kwargs)
        raise Http404

    def get_object_list(self, collection):
        obj_list = db.collection(collection)\
            .where('owner_id', '==', self.query_user['localId']).get()
        return [obj.to_dict() for obj in obj_list]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_user'] = self.query_user
        context['certs'] = self.get_object_list('certs')
        context['skills'] = self.get_object_list('skills')
        return context

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

def parse_id_token(token: str) -> dict:
    import base64, json
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("Incorrect id token format")

    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)

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
        # Create user session
        session_data = parse_id_token(r.get('idToken'))
        session = db.collection('sessions').add(session_data)[1]
        response = HttpResponseRedirect(self.success_url)
        response.set_cookie('sessionid', value=session._path[1])
        return response
"""
class LoginWithGoogle(generic.UnauthenticatedMixin, RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        url = 'https://oauth2.googleapis.com/token'
        code = request.GET.get('code')
        data = '{ "code" : "' + code + '", '\
            + '"client_id" : "' + settings.OAUTH_CLIENT_ID + '", '\
            + '"client_secret" : "' + settings.OAUTH_CLIENT_SECRET + '", '\
            + '"redirect_uri" : "http://localhost:8000/get-id-token", '\
            + '"grant_type" : "authorization_code" }'
        r = requests.post(url, data).json()
        print(r)
        return super().get(request, *args, **kwargs)

class GetIdToken(generic.UnauthenticatedMixin, RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key='\
            + settings.FIREBASE_WEB_API_TOKEN
        requestUri = request.build_absolute_uri(request.get_full_path())
        id_token = request.GET.get('id_token')
        data = '{ "requestUri" : "' + requestUri + '" , "postBody" : "id_token='\
            + id_token + '&providerId=google.com",\
            "returnSecureToken" : true, "returnIdpCredential" : true }'
        r = requests.post(url, data)
        return super().get(request, *args, **kwargs)
"""

class Logout(generic.AuthenticatedMixin, RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        """Delete current auth session and cookie"""
        try:
            sid = request.COOKIES['sessionid']
            db.collection('sessions').document(sid).delete()
            del request.COOKIES['sessionid']
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
        