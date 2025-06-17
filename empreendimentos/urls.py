from django.urls import path
from . import views

# O nome do app é usado para namespacing de URLs, ex: 'empreendimentos:detail'
app_name = 'empreendimentos'

urlpatterns = [
    # A rota para a lista de empreendimentos
    path('', views.empreendimento_list, name='list'),
    # A rota para os detalhes de um empreendimento específico
    path('<slug:slug>/', views.empreendimento_detail, name='detail'),
]