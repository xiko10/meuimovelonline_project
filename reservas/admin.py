# reservas/admin.py

from django.contrib import admin
from .models import Lead, Reserva, InteracaoLead, DocumentoReserva, HistoricoStatusReserva

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # AQUI ESTÁ A CORREÇÃO: Adicionamos 'corretor_origem_link' ao list_display
    list_display = ('id', 'nome_cliente', 'unidade_interesse', 'status', 'origem', 'corretor_atribuido', 'corretor_origem_link', 'data_criacao')
    list_filter = ('status', 'origem', 'data_criacao')
    search_fields = ('nome_cliente', 'email_cliente', 'cpf_cliente')
    list_per_page = 20

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'unidade', 'cliente', 'corretor', 'status', 'data_atualizacao')
    list_filter = ('status', 'data_criacao')
    search_fields = ('cliente__first_name', 'cliente__last_name', 'unidade__empreendimento__nome')
    autocomplete_fields = ['unidade', 'cliente', 'corretor'] # Facilita a busca
    list_per_page = 20

@admin.register(InteracaoLead)
class InteracaoLeadAdmin(admin.ModelAdmin):
    list_display = ('lead', 'usuario', 'data_interacao')
    list_filter = ('data_interacao',)
    search_fields = ('lead__nome_cliente',)

# Registrando os outros modelos de forma simples
admin.site.register(DocumentoReserva)
admin.site.register(HistoricoStatusReserva)