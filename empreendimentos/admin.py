# empreendimentos/admin.py (VERSÃO COMPLETA E FINAL)

from django.contrib import admin
from .models import (
    Empreendimento, 
    Unidade, 
    Amenidade, 
    FiltroLocalizacao, 
    ProgramaHabitacional,
    Parceria, # Importando o modelo que faltava
    ImagemEmpreendimento,
    VideoEmpreendimento,
    DocumentoEmpreendimento,
    EmpreendimentoFiltro,
    FluxoPagamento
)

class ParceriaAdmin(admin.ModelAdmin):
    list_display = ('empreendimento', 'imobiliaria', 'status', 'data_convite', 'data_resposta')
    list_filter = ('status',)
    search_fields = ('empreendimento__nome', 'imobiliaria__nome')

class UnidadeAdmin(admin.ModelAdmin):
    search_fields = ('empreendimento__nome', 'id')
    list_display = ('id', 'empreendimento', 'tipo', 'status', 'valor_total')
    list_filter = ('status', 'tipo')

# Registrando todos os modelos para que sejam visíveis no admin
admin.site.register(Empreendimento)
admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Amenidade)
admin.site.register(FiltroLocalizacao)
admin.site.register(ProgramaHabitacional)
admin.site.register(Parceria, ParceriaAdmin) # Registrando o modelo Parceria com sua configuração

# Registrando outros modelos para facilitar a depuração, se necessário
admin.site.register(ImagemEmpreendimento)
admin.site.register(VideoEmpreendimento)
admin.site.register(DocumentoEmpreendimento)
admin.site.register(EmpreendimentoFiltro)
admin.site.register(FluxoPagamento)