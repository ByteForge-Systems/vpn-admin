from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin-2fa/', views.admin_2fa_view, name='admin_2fa'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('servers/', views.servers, name='servers'),
    path('deploy/', views.deploy, name='deploy')
]
