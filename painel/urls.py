# painel/urls.py (VERSÃO COMPLETA E CORRIGIDA)

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.painel_redirect_view, name='painel_redirect'),

    # --- ROTAS DO SUPER ADMIN ---
    path('admin/', include([
        path('', views.admin_dashboard, name='admin_dashboard'),
    ])),

    # --- ROTAS DO ANUNCIANTE ---
    path('anunciante/', include([
        path('', views.anunciante_dashboard, name='anunciante_dashboard'),
        path('empreendimentos/novo/', views.anunciante_empreendimento_create, name='anunciante_empreendimento_create'),
        path('empreendimentos/<int:pk>/editar/etapa<int:step>/', views.anunciante_empreendimento_update, name='anunciante_empreendimento_update'),
        path('leads/', views.anunciante_lead_list, name='anunciante_lead_list'),
        path('reservas/', views.anunciante_reserva_list, name='anunciante_reserva_list'),
        path('reservas/<int:pk>/', views.anunciante_reserva_detail, name='anunciante_reserva_detail'),
    ])),

    # --- ROTAS DO ADMIN DE IMOBILIÁRIA ---
    path('imobiliaria/', include([
        path('', views.imobiliaria_dashboard, name='imobiliaria_dashboard'),
    ])),

    # --- ROTAS DO GERENTE DE IMOBILIÁRIA ---
    path('gerente/', include([
        path('', views.gerente_dashboard, name='gerente_dashboard'),
    ])),
    
    # --- ROTAS DO CORRETOR ---
    path('corretor/', include([
        path('', views.corretor_dashboard, name='corretor_dashboard'),
        path('leads/', views.corretor_lead_list, name='corretor_lead_list'),
        path('reservas/', views.corretor_reserva_list, name='corretor_reserva_list'),
    ])),

    # --- ROTAS DO CLIENTE ---
    # (A rota do cliente será '/painel/cliente/reservas/', a ser criada com as views de reserva)
]