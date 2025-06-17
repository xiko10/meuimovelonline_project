# core/admin.py (VERSÃO CORRIGIDA)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Imobiliaria

class CustomUserAdmin(UserAdmin):
    """
    Configuração para exibir e editar nosso campo 'perfil' na área admin.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'perfil')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Controle de Perfil', {'fields': ('perfil', 'imobiliaria')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Controle de Perfil', {'fields': ('perfil', 'imobiliaria')}),
    )

    # LINHA ADICIONADA: Define os campos para a busca inteligente de usuários
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.register(Imobiliaria)
admin.site.register(User, CustomUserAdmin)