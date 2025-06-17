# core/urls.py (VERSÃO CORRIGIDA)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Este arquivo agora cuida apenas das rotas PÚBLICAS e de autenticação.
urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]