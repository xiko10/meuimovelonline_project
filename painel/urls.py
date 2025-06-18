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
        path('empreendimentos/', views.anunciante_empreendimento_list, name='anunciante_empreendimento_list'),
        path('empreendimentos/novo/', views.anunciante_empreendimento_create, name='anunciante_empreendimento_create'),
        path('empreendimentos/<int:pk>/editar/etapa<int:step>/', views.anunciante_empreendimento_update, name='anunciante_empreendimento_update'),
        path('leads/', views.anunciante_lead_list, name='anunciante_lead_list'),
        path('leads/atribuir/<int:lead_id>/', views.anunciante_atribuir_lead, name='anunciante_atribuir_lead'),
        path('reservas/', views.anunciante_reserva_list, name='anunciante_reserva_list'),
        path('reservas/<int:pk>/', views.anunciante_reserva_detail, name='anunciante_reserva_detail'),
        path('reservas/<int:pk>/alterar-status/<str:novo_status>/', views.anunciante_alterar_status_reserva, name='anunciante_alterar_status_reserva'),
        path('parceiros/', views.anunciante_parceiros_list, name='anunciante_parceiros_list'),
        path('parceiros/convidar/<int:imobiliaria_id>/', views.anunciante_convidar_parceiro, name='anunciante_convidar_parceiro'),
        path('analytics/', views.anunciante_analytics_view, name='anunciante_analytics'),
        path('configuracoes/', views.anunciante_configuracoes_view, name='anunciante_configuracoes'),
    ])),

    # --- ROTAS DO ADMIN DE IMOBILIÁRIA ---
    path('imobiliaria/', include([
        path('', views.imobiliaria_dashboard, name='imobiliaria_dashboard'),
        path('parcerias/', views.imobiliaria_parcerias_list, name='imobiliaria_parcerias_list'),
        path('parcerias/responder/<int:parceria_id>/<str:resposta>/', views.imobiliaria_responder_convite, name='imobiliaria_responder_convite'),
        path('equipe/', views.imobiliaria_equipe_list, name='imobiliaria_equipe_list'),
        path('equipe/novo/', views.imobiliaria_membro_create, name='imobiliaria_membro_create'),
        path('materiais/', views.imobiliaria_materiais_list, name='imobiliaria_materiais_list'),
    ])),

    # --- ROTAS DO GERENTE DE IMOBILIÁRIA ---
    path('gerente/', include([
        path('', views.gerente_dashboard, name='gerente_dashboard'),
    ])),
    
    # --- ROTAS DO CORRETOR ---
    path('corretor/', include([
        path('', views.corretor_dashboard, name='corretor_dashboard'),
        path('leads/', views.corretor_lead_list, name='corretor_lead_list'),
        path('leads/<int:lead_id>/', views.corretor_lead_detail, name='corretor_lead_detail'),
        path('materiais/', views.corretor_materiais_list, name='corretor_materiais_list'),
        path('reservas/', views.corretor_reserva_list, name='corretor_reserva_list'),
        path('reservas/<int:pk>/', views.corretor_reserva_detail, name='corretor_reserva_detail'),

    ])),

    # --- ROTAS DO CLIENTE ---
    # (A rota do cliente será '/painel/cliente/reservas/', a ser criada com as views de reserva)
]