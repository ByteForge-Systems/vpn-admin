from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('servers/', views.servers, name='servers'),
    path('deploy/', views.deploy, name='deploy'),
    path('2fa/', views.two_factor_view, name='two_factor')
]
