# core/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rota para a página inicial pública
    path('', views.home_page, name='home'),

    # Rota para a página de login. Usaremos a view nativa do Django,
    # apenas apontando para o nosso template customizado.
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    # Rota para a ação de logout. A view nativa do Django cuida de tudo.
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Rota "inteligente" que redirecionará o usuário para o painel correto após o login.
    path('painel/', views.painel_redirect_view, name='painel_redirect'),
]