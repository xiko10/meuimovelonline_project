from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_page(request):
    """
    Renderiza a página inicial pública da plataforma.
    """
    return render(request, 'core/home.html')

@login_required
def painel_redirect_view(request):
    """
    Redireciona o usuário logado para o dashboard correspondente ao seu perfil.
    Esta é a implementação da nossa regra de negócio de redirecionamento.
    """
    perfil = request.user.perfil

    if perfil == 'superadmin':
        return redirect('admin_dashboard') # Futura rota do painel admin
    elif perfil == 'anunciante':
        return redirect('anunciante_dashboard') # Futura rota do painel anunciante
    elif perfil == 'admin_imob':
        return redirect('imobiliaria_dashboard') # Futura rota do painel imobiliária
    elif perfil == 'gerente':
        return redirect('gerente_dashboard') # Futura rota do painel gerente
    elif perfil == 'corretor':
        return redirect('corretor_dashboard') # Futura rota do painel corretor
    elif perfil == 'cliente':
        return redirect('cliente_reserva_list') # Futura rota do painel cliente
    else:
        # Caso o usuário não tenha perfil (ou para um fallback), redireciona para a home.
        return redirect('home')