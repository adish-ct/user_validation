from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# @cache_control(no_cache=True, no_store=True)

# user authentication method provided by django

# Create your views here.

# def home(request):
#     return render(request, "login/index.html")
#
#
# def signup(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         username = request.POST['username']
#         phone = request.POST['phone']
#         email = request.POST.get('email')
#         password = request.POST['password']
#         re_password = request.POST.get('repassword')
#
#         if password == re_password:
#             my_user = User.objects.create_user(username, email, password)
#             my_user.phone = phone
#             my_user.save()
#             messages.success(request, "Registration Successful")
#             return redirect('login_app:signin')
#         else:
#             messages.error(request, "Password is not matching try again...")
#             return redirect(signup)
#
#     return render(request, "login/signup.html")
#
#
# def signin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # authenticate the user and check it is valid or not
#         user = authenticate(username=username, password=password)
#
#         # if the user is valid allow to login user and else push and error message
#         if user is not None:
#             login(request, user)
#             userid = user.username
#             messages.success(request, "log in successfully..")
#             # return render(request, 'login/index.html', {'userid': userid})
#             context = {'userid': userid}
#
#             # redirect_page = render(request, 'login/index.html', {'userid': userid})
#             return redirect(home)
#
#         else:
#             messages.error(request, "User name and Password is not matching")
#             return redirect('/')
#
#     return render(request, "login/signin.html")
#
#
# def signout(request):
#     logout(request)
#     messages.success(request, "Logged out successfully")
#     return redirect(signin)


@cache_control(no_cache=True, no_store=True)
def home(request):
    if 'username' in request.session:
        return redirect(main_page)
    return render(request, 'login/index.html')


@cache_control(no_cache=True, no_store=True)
def signup(request):
    if 'username' in request.session:
        return redirect(main_page)
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['repassword']

        if password == c_password:
            my_user = User.objects.create_user(username, email, password)
            my_user.phone = phone
            my_user.save()
            messages.success(request, "successfully created your account...")
            return redirect(signin)
        else:
            messages.error(request, "password is not matching, try again...")
            return redirect(signup)
    return render(request, 'login/signup.html')


@cache_control(no_cache=True, no_store=True)
def signin(request):
    if 'username' in request.session:
        return redirect(main_page)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:
                request.session['username'] = username
                return redirect(main_page)
            else:
                messages.error(request, "invalid credentials")
                return redirect(signin)

    return render(request, 'login/signin.html')


@cache_control(no_cache=True, no_store=True)
def signout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect(signin)


@cache_control(no_cache=True, no_store=True)
def main_page(request):
    if 'username' in request.session:
        username = request.session['username']
        return render(request, 'login/home.html', {'username': username})
    else:
        return redirect(home)
