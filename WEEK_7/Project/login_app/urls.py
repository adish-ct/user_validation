from django.urls import path
from . import views

# app_name = 'login_app'

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('main_page/', views.main_page, name="main_page"),

]