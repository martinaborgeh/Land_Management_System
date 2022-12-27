from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('base/', views.basehtmlrender),
    path('homepage/', views.homepage,name='homepage'),
    path('register/', views.registration, name='register'),
    path('SearchDetails/', views.GetDetailsFromUSer, name='Search'),
    path('DisplayDetails/', views.sendDetailsToUser, name='Display'),
    path('Profile/',views.profile, name='profile'),
    path('wrongid/',views.wrongparcelid, name = 'wrongid'),
    path('Login/', auth_views.LoginView.as_view(template_name ='Login.html'), name='Login'),
    path('Login/', auth_views.LogoutView.as_view(template_name ='Login.html'), name='Logout'),

]