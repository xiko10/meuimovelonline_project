# empreendimentos/admin.py (VERSÃO CORRIGIDA E COMPLETA)

from django.contrib import admin
from .models import Empreendimento, Unidade, Amenidade, FiltroLocalizacao, ProgramaHabitacional

# Registramos todos os modelos de base para que sejam gerenciáveis no /superadmin/
admin.site.register(Empreendimento)
admin.site.register(Unidade)
admin.site.register(Amenidade)
admin.site.register(FiltroLocalizacao)
admin.site.register(ProgramaHabitacional)