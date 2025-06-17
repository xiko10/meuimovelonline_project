# 1. Importações do Django
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

# 2. Importações dos nossos próprios arquivos
from core.decorators import *
# AQUI ESTÁ A CORREÇÃO: A lista de importação agora inclui TODOS os formulários do assistente
from empreendimentos.forms import (
    EmpreendimentoEtapaInicialForm, 
    EmpreendimentoEtapa3Form,
    EmpreendimentoEtapa6Form, 
    EmpreendimentoEtapa7Form,
    EmpreendimentoEtapa8Form, # <<<<<< FORMULÁRIO FALTANTE ADICIONADO
    ImagemEmpreendimentoFormSet, 
    VideoEmpreendimentoFormSet, 
    DocumentoEmpreendimentoFormSet,
    UnidadeFormSet,
    EmpreendimentoFiltroFormSet,
    FluxoPagamentoFormSet
)
from empreendimentos.models import Empreendimento

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
    # ... (código existente)
    if request.method == 'POST':
        form = EmpreendimentoEtapaInicialForm(request.POST) 
        if form.is_valid():
            empreendimento = form.save(commit=False)
            empreendimento.anunciante_responsavel = request.user
            form.save(commit=True)
            return redirect(reverse('anunciante_empreendimento_update', kwargs={'pk': empreendimento.pk, 'step': 3}))
    else:
        form = EmpreendimentoEtapaInicialForm() 
    context = {'form': form, 'step': 'Inicial'}
    return render(request, 'painel/anunciante/empreendimento_form.html', context)

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
    empreendimento = get_object_or_404(Empreendimento, pk=pk)
    
    # Mapeamento de Etapas para Formulários e Formsets
    step_map = {
        3: {'form': EmpreendimentoEtapa3Form, 'formsets': {}, 'next_step': 4},
        4: {'form': None, 'formsets': {'imagens': ImagemEmpreendimentoFormSet, 'videos': VideoEmpreendimentoFormSet, 'documentos': DocumentoEmpreendimentoFormSet}, 'next_step': 5},
        5: {'form': None, 'formsets': {'unidades': UnidadeFormSet}, 'next_step': 6},
        6: {'form': EmpreendimentoEtapa6Form, 'formsets': {'filtros_proximidade': EmpreendimentoFiltroFormSet}, 'next_step': 7},
        7: {'form': EmpreendimentoEtapa7Form, 'formsets': {'fluxo_pagamento': FluxoPagamentoFormSet}, 'next_step': 8},
        8: {'form': EmpreendimentoEtapa8Form, 'formsets': {}, 'next_step': None}, # Etapa final
    }

    if step not in step_map:
        return redirect(reverse('anunciante_empreendimento_update', kwargs={'pk': pk, 'step': 3}))

    current_step_config = step_map[step]
    FormClass = current_step_config['form']
    formset_configs = current_step_config['formsets']
    
    # Define a URL de destino
    if current_step_config['next_step']:
        next_step_url = reverse('anunciante_empreendimento_update', kwargs={'pk': pk, 'step': current_step_config['next_step']})
    else:
        next_step_url = reverse('anunciante_dashboard') # Destino final

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=empreendimento) if FormClass else None
        
        formsets = {}
        for key, fs_class in formset_configs.items():
            formsets[key] = fs_class(request.POST, request.FILES, instance=empreendimento)

        # Validação
        form_is_valid = form.is_valid() if form else True
        formsets_are_valid = all(fs.is_valid() for fs in formsets.values())

        if form_is_valid and formsets_are_valid:
            if form:
                form.save()
            for fs in formsets.values():
                fs.save()
            
            # Lógica especial para salvar o status na Etapa 8
            if step == 8:
                empreendimento.status_publicacao = form.cleaned_data.get('status_publicacao', 'rascunho')
                empreendimento.save()

            return redirect(next_step_url)

    else: # GET request
        form = FormClass(instance=empreendimento) if FormClass else None
        formsets = {}
        for key, fs_class in formset_configs.items():
            formsets[key] = fs_class(instance=empreendimento)

    context = {
        'form': form,
        'formsets': formsets,
        'step': step,
        'empreendimento': empreendimento,
    }
    return render(request, 'painel/anunciante/empreendimento_form.html', context)