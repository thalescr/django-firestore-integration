from datetime import datetime
from django.shortcuts import redirect

## Ensure user has a valid cookie
def authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        cookie = request.session.get('sessionid', False)
        if cookie:
            #if datetime.now() < cookie.get_expiry_date():
            return view_func(request, *args, *kwargs)
        return redirect('login')
    return wrapper_func

## Ensure user is not authenticated
def not_authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        cookie = request.session.get('sessionid', False)
        if cookie:
            #if datetime.now() < cookie.get_expiry_date():
            return redirect('home')
        return view_func(request, *args, *kwargs)
    return wrapper_func