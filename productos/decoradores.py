from django.shortcuts import redirect

def login_requerido(func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper
