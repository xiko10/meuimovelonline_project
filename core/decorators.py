# core/decorators.py

# Este arquivo contém as funções de teste para o decorator @user_passes_test.
# Elas verificam se o usuário está autenticado e se possui o perfil correto.

def is_superadmin(user):
    return user.is_authenticated and user.perfil == 'superadmin'

def is_anunciante(user):
    return user.is_authenticated and user.perfil == 'anunciante'

def is_gerente_anunciante(user):
    return user.is_authenticated and user.perfil == 'gerente_anunciante'

def is_admin_imob(user):
    return user.is_authenticated and user.perfil == 'admin_imob'

def is_gerente(user):
    return user.is_authenticated and user.perfil == 'gerente'

def is_corretor(user):
    return user.is_authenticated and user.perfil == 'corretor'

def is_cliente(user):
    return user.is_authenticated and user.perfil == 'cliente'

def is_anunciante_ou_superadmin(user):
    """Verifica se o usuário é Anunciante OU Super Admin."""
    return user.is_authenticated and (user.perfil == 'anunciante' or user.perfil == 'superadmin')