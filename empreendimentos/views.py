# empreendimentos/views.py

from django.shortcuts import render, get_object_or_404
from .models import Empreendimento

def empreendimento_list(request):
    """
    Exibe a lista de todos os empreendimentos com status 'publicado'.
    """
    empreendimentos = Empreendimento.objects.filter(status_publicacao='publicado')
    context = {
        'empreendimentos': empreendimentos
    }
    return render(request, 'empreendimentos/empreendimento_list.html', context)

def empreendimento_detail(request, slug):
    """
    Exibe os detalhes de um único empreendimento, identificado pelo seu slug.
    """
    empreendimento = get_object_or_404(Empreendimento, slug=slug, status_publicacao='publicado')
    context = {
        'empreendimento': empreendimento
    }
    return render(request, 'empreendimentos/empreendimento_detail.html', context)