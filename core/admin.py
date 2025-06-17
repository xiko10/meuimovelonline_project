from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Imobiliaria

class CustomUserAdmin(UserAdmin):
    """
    Configuração para exibir e editar nosso campo 'perfil' na área admin.
    """
    # Adiciona o campo 'perfil' aos campos exibidos na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'perfil')
    
    # Adiciona o campo 'perfil' ao formulário de edição de usuário
    # (copiamos os fieldsets padrão e adicionamos o nosso)
    fieldsets = UserAdmin.fieldsets + (
        ('Controle de Perfil', {'fields': ('perfil',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Controle de Perfil', {'fields': ('perfil',)}),
    )

# Registra nosso modelo de Imobiliária para que apareça no admin
admin.site.register(Imobiliaria)
# Registra nosso modelo User com a configuração customizada acima
admin.site.register(User, CustomUserAdmin)