from django.contrib.auth import get_user_model, login, authenticate, logout
from django.shortcuts import render, redirect

from .models import MyUser
User = get_user_model()


# Create your views here.
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(email=email, username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')