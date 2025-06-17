# painel/views.py (VERSÃO FINAL COM IMPORTAÇÕES CORRIGIDAS)

# 1. Importações do Django
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

# 2. Importações dos nossos próprios arquivos
from core.decorators import *
# AQUI ESTÁ A CORREÇÃO: Importamos o formulário unificado e o da etapa 3
from empreendimentos.models import Empreendimento
from empreendimentos.forms import (
    EmpreendimentoEtapaInicialForm, EmpreendimentoEtapa3Form,
    ImagemEmpreendimentoFormSet, VideoEmpreendimentoFormSet, DocumentoEmpreendimentoFormSet
)

# -----------------------------------------------------------------------------
# VIEW DE REDIRECIONAMENTO PRINCIPAL (permanece igual)
# -----------------------------------------------------------------------------
@login_required
def painel_redirect_view(request):
    perfil = request.user.perfil
    if perfil == 'superadmin':
        return redirect('admin_dashboard')
    elif perfil == 'anunciante':
        return redirect('anunciante_dashboard')
    # ... (outros redirecionamentos)
    else:
        return redirect('home')

# -----------------------------------------------------------------------------
# VIEWS DE PLACEHOLDER PARA OS DASHBOARDS (permanecem iguais)
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_superadmin)
def admin_dashboard(request):
    return HttpResponse("Painel do Super Admin em construção.")

# ... (todas as outras views de dashboard de placeholder permanecem aqui) ...

@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_dashboard(request):
    return HttpResponse("Painel do Anunciante em construção.")

@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_dashboard(request):
    return HttpResponse("Painel do Admin de Imobiliária em construção.")

@login_required
@user_passes_test(is_gerente)
def gerente_dashboard(request):
    return HttpResponse("Painel do Gerente de Imobiliária em construção.")

@login_required
@user_passes_test(is_corretor)
def corretor_dashboard(request):
    return HttpResponse("Painel do Corretor em construção.")

# -----------------------------------------------------------------------------
# VIEWS DO ASSISTENTE DE CRIAÇÃO (COM A REFERÊNCIA AO FORMULÁRIO CORRIGIDA)
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_empreendimento_create(request):
    """
    View para a ETAPA INICIAL UNIFICADA de criação.
    """
    if request.method == 'POST':
        # AQUI ESTÁ A CORREÇÃO: Usamos o novo nome do formulário
        form = EmpreendimentoEtapaInicialForm(request.POST) 
        if form.is_valid():
            empreendimento = form.save(commit=False)
            empreendimento.anunciante_responsavel = request.user
            form.save(commit=True)
            # Redireciona para a Etapa 3, que é a próxima etapa lógica
            return redirect(reverse('anunciante_empreendimento_update', kwargs={'pk': empreendimento.pk, 'step': 3}))
    else:
        # E AQUI TAMBÉM:
        form = EmpreendimentoEtapaInicialForm() 
    
    context = {'form': form, 'step': 'Inicial'}
    return render(request, 'painel/anunciante/empreendimento_form.html', context)


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_empreendimento_update(request, pk, step):
    """
    View principal do assistente, agora com lógica para a Etapa 4.
    """
    empreendimento = get_object_or_404(Empreendimento, pk=pk)
    
    # Dicionário para guardar os formsets da etapa atual
    formsets = {}
    
    if step == 3:
        FormClass = EmpreendimentoEtapa3Form
        next_step_url = reverse('anunciante_empreendimento_update', kwargs={'pk': pk, 'step': 4})
    elif step == 4:
        # Na Etapa 4, não temos um formulário principal, apenas formsets
        FormClass = None 
        # Instanciamos os formsets para Mídias e Documentos
        formsets['imagens'] = ImagemEmpreendimentoFormSet(instance=empreendimento)
        formsets['videos'] = VideoEmpreendimentoFormSet(instance=empreendimento)
        formsets['documentos'] = DocumentoEmpreendimentoFormSet(instance=empreendimento)
        next_step_url = reverse('anunciante_empreendimento_update', kwargs={'pk': pk, 'step': 5})
    # (Futuramente, adicionaremos elif para as etapas 5, 6, etc. aqui)
    else:
        # Redireciona para a primeira etapa de edição (a 3, que é a próxima após a inicial)
        return redirect(reverse('anunciante_empreendimento_update', kwargs={'pk': pk, 'step': 3}))

    if request.method == 'POST':
        # Se a etapa tem um formulário principal, processa-o
        form = FormClass(request.POST, request.FILES, instance=empreendimento) if FormClass else None

        if step == 4:
            # Lógica especial para processar múltiplos formsets na Etapa 4
            formsets['imagens'] = ImagemEmpreendimentoFormSet(request.POST, request.FILES, instance=empreendimento)
            formsets['videos'] = VideoEmpreendimentoFormSet(request.POST, request.FILES, instance=empreendimento)
            formsets['documentos'] = DocumentoEmpreendimentoFormSet(request.POST, request.FILES, instance=empreendimento)
            
            if all(fs.is_valid() for fs in formsets.values()):
                for fs in formsets.values():
                    fs.save()
                return redirect(next_step_url)
        
        elif form and form.is_valid():
            form.save()
            return redirect(next_step_url)
    else:
        # Se a etapa tem um formulário principal, instancia-o
        form = FormClass(instance=empreendimento) if FormClass else None

    context = {
        'form': form,
        'formsets': formsets, # Passa os formsets para o template
        'step': step,
        'empreendimento': empreendimento,
    }
    return render(request, 'painel/anunciante/empreendimento_form.html', context)