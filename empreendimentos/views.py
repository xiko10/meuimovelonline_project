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
    empreendimento = get_object_or_404(Empreendimento, slug=slug, status_publicacao='publicado')
    
    # Pega o username do corretor do parâmetro 'ref' na URL, se existir
    ref_corretor_username = request.GET.get('ref', None)

    context = {
        'empreendimento': empreendimento,
        'ref_corretor': ref_corretor_username, # Passa o username para o template
    }
    return render(request, 'empreendimentos/empreendimento_detail.html', context)