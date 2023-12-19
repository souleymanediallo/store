from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from .models import MyUser, ShippingAddress
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


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, 'accounts/profile-update.html', context)


@login_required
def address(request):
    addresses = request.user.addresses.all()
    context = {"addresses": addresses}
    return render(request, 'accounts/address.html', context)


@login_required
def set_default_shipping(request, pk):
    address: ShippingAddress = get_object_or_404(ShippingAddress, pk=pk)
    address.set_default()
    return redirect('address')


@login_required
def address_delete(request, pk):
    address: ShippingAddress = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    address.delete()
    return redirect('address')