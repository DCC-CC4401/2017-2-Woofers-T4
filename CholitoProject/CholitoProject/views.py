from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from CholitoProject.userManager import get_user_index


def home(request):
    return redirect('user-home')


# TODO: redirect to correct template

class AuthView(View):
    @csrf_exempt
    def post(self, request, **kwargs):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            current_user = get_user_index(user)
            if current_user is not None:
                login(request, user)
                return redirect('/')

        messages.error(request,
                       "La combinación de usuario y contraseña no coincide")
        return redirect('/login/')


class LogOutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/')
