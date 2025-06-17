# core/views.py (VERSÃO CORRIGIDA E LIMPA)

from django.shortcuts import render

def home_page(request):
    """
    Renderiza a página inicial pública da plataforma.
    """
    # Adicionaremos aqui a lógica de busca da home no futuro.
    return render(request, 'core/home.html')