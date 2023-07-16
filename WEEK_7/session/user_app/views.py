from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# @cache_control(no_cache=True, no_store=True)
# Create your views here.


@cache_control(no_cache=True, no_store=True)
def log_in(request):
    if 'username' in request.session:
        return redirect(home)
    else:
        if request.method == 'POST':
            try:
                username = request.POST['user_name']
            except:
                print("username error")
            password = request.POST['user_password']
            user = authenticate(request, username=username, password=password)
            if user:
                request.session['username'] = username
                login(request, user)
                return redirect(home)
            else:
                messages.error(request, "Username and password not matching")
                return redirect(log_in)
    return render(request, 'login.html')


@cache_control(no_cache=True, no_store=True)
def sign_up(request):
    if 'username' in request.session:
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            c_password = request.POST.get('c_password')

            if password == c_password:
                my_user = User.objects.create_user(username=username, password=password, email=email)
                my_user.save()
                messages.success(request, "User created successfully ")
                return redirect(log_in)
            else:
                messages.error(request, "Password didn't match, try again")
                return redirect(sign_up)

    return render(request, 'signup.html')


@login_required(login_url='log_in')
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect(log_in)
    else:
        return redirect(home)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='log_in')
def home(request):
    username = request.session['username']
    return render(request, 'home.html', {'username': username})


def error_404(request, exception):
    return render(request, '404.html')


@login_required(login_url='log_in')
def sample(request):
    return render(request, 'sample.html')
