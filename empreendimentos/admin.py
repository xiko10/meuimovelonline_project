# empreendimentos/admin.py (VERSÃO CORRIGIDA)

from django.contrib import admin
from .models import Empreendimento, Unidade, Amenidade, FiltroLocalizacao, ProgramaHabitacional

class UnidadeAdmin(admin.ModelAdmin):
    # Define os campos para a busca inteligente de unidades
    search_fields = ('empreendimento__nome', 'id')
    list_display = ('id', 'empreendimento', 'tipo', 'status', 'valor_total')
    list_filter = ('status', 'tipo')

# Registrando os modelos
admin.site.register(Empreendimento)
admin.site.register(Unidade, UnidadeAdmin) # Registra Unidade com a configuração customizada
admin.site.register(Amenidade)
admin.site.register(FiltroLocalizacao)
admin.site.register(ProgramaHabitacional)