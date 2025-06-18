from django.utils import timezone
from django.db.models import Q
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.decorators import *
from empreendimentos.forms import (
    EmpreendimentoEtapaInicialForm, 
    EmpreendimentoEtapa3Form,
    EmpreendimentoEtapa6Form, 
    EmpreendimentoEtapa7Form,
    EmpreendimentoEtapa8Form, 
    ImagemEmpreendimentoFormSet, 
    VideoEmpreendimentoFormSet, 
    DocumentoEmpreendimentoFormSet,
    UnidadeFormSet,
    EmpreendimentoFiltroFormSet,
    FluxoPagamentoFormSet
)
from empreendimentos.models import Empreendimento
from reservas.models import Lead, Reserva, HistoricoStatusReserva, InteracaoLead
from core.models import Imobiliaria, User
from empreendimentos.models import Parceria
from reservas.forms import AtribuirLeadForm, InteracaoLeadForm
from reservas.forms import DocumentoReservaUploadForm
from .forms import MembroImobiliariaCreationForm
from empreendimentos.forms import MaterialVendaForm
from empreendimentos.models import MaterialVenda



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
    elif perfil == 'admin_imob':
        return redirect('imobiliaria_dashboard')
    elif perfil == 'gerente':
        return redirect('gerente_dashboard')
    elif perfil == 'corretor':
        return redirect('corretor_dashboard')
    elif perfil == 'cliente':
        return redirect('cliente_reserva_list')
    else:
        return redirect('home')

# -----------------------------------------------------------------------------
# VIEWS DE PLACEHOLDER PARA OS DASHBOARDS (permanecem iguais)
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_superadmin)
def admin_dashboard(request):
    return render(request, 'painel/admin/admin_dashboard.html')

# ... (todas as outras views de dashboard de placeholder permanecem aqui) ...

@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_dashboard(request):
    return render(request, 'painel/anunciante/anunciante_dashboard.html')

@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_dashboard(request):
    return render(request, 'painel/imobiliaria/imobiliaria_dashboard.html')

@login_required
@user_passes_test(is_gerente)
def gerente_dashboard(request):
    return render(request, 'painel/gerente/gerente_dashboard.html')

@login_required
@user_passes_test(is_corretor)
def corretor_dashboard(request):
    return render(request, 'painel/corretor/corretor_dashboard.html')

# -----------------------------------------------------------------------------
# VIEWS DO ASSISTENTE DE CRIAÇÃO (COM A REFERÊNCIA AO FORMULÁRIO CORRIGIDA)
# -----------------------------------------------------------------------------
@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_empreendimento_create(request):
    if request.method == 'POST':
        form = EmpreendimentoEtapaInicialForm(request.POST) 
        if form.is_valid():
            empreendimento = form.save(commit=False)
            empreendimento.anunciante_responsavel = request.user
            form.save(commit=True)
            return redirect(reverse('anunciante_empreendimento_update', kwargs={'pk': empreendimento.pk, 'step': 3}))
    else:
        form = EmpreendimentoEtapaInicialForm() 
    return render(request, 'painel/anunciante/empreendimento_form.html', {'form': form, 'step': 'Inicial'})


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
        return render(request, 'painel/anunciante/empreendimento_form.html', context)


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


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_lead_list(request):
    # Filtra os leads para mostrar apenas aqueles dos empreendimentos do anunciante logado
    leads = Lead.objects.filter(unidade_interesse__empreendimento__anunciante_responsavel=request.user).order_by('-data_criacao')
    context = {
        'leads': leads
    }
    return render(request, 'painel/anunciante/anunciante_lead_list.html', context)

@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_reserva_list(request):
    # Filtra as reservas para mostrar apenas aquelas dos empreendimentos do anunciante logado
    reservas = Reserva.objects.filter(unidade__empreendimento__anunciante_responsavel=request.user).order_by('-data_atualizacao')
    context = {
        'reservas': reservas
    }
    return render(request, 'painel/anunciante/anunciante_reserva_list.html', {'reservas': reservas})


@login_required
@user_passes_test(is_corretor)
def corretor_lead_list(request):
    # Usamos o objeto Q para criar uma consulta OR:
    # (corretor_atribuido É o usuário logado) OU (corretor_origem_link É o usuário logado)
    leads = Lead.objects.filter(
        Q(corretor_atribuido=request.user) | Q(corretor_origem_link=request.user)
    ).distinct().order_by('-data_criacao')
    
    context = {'leads': leads}
    return render(request, 'painel/corretor/corretor_lead_list.html', context)

@login_required
@user_passes_test(is_corretor)
def corretor_reserva_list(request):
    # Mostra apenas as reservas realizadas pelo corretor logado
    reservas = Reserva.objects.filter(corretor=request.user).order_by('-data_atualizacao')
    context = {'reservas': reservas}
    return render(request, 'painel/corretor/corretor_reserva_list.html', context)


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_reserva_detail(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, unidade__empreendimento__anunciante_responsavel=request.user)
    
    # Formulário para upload de um novo documento
    upload_form = DocumentoReservaUploadForm()

    if request.method == 'POST':
        # Esta parte processa o formulário de upload
        upload_form = DocumentoReservaUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            documento = upload_form.save(commit=False)
            documento.reserva = reserva
            documento.uploaded_por = request.user
            documento.save()
            messages.success(request, f"Documento '{documento.nome_documento}' enviado com sucesso!")
            return redirect('anunciante_reserva_detail', pk=reserva.pk)

    # Pega a lista de documentos já enviados para esta reserva
    documentos_enviados = reserva.documentos.all()
    
    context = {
        'reserva': reserva,
        'documentos': documentos_enviados,
        'upload_form': upload_form, # Passa o formulário para o template
    }
    return render(request, 'painel/anunciante/anunciante_reserva_detail.html', context)


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_alterar_status_reserva(request, pk, novo_status):
    """
    Processa a alteração de status de uma reserva.
    Ação disponível apenas via método POST para segurança.
    """
    if request.method == 'POST':
        # Garante que o anunciante só pode alterar reservas de seus próprios empreendimentos
        reserva = get_object_or_404(Reserva, pk=pk, unidade__empreendimento__anunciante_responsavel=request.user)
        
        status_anterior = reserva.get_status_display()
        reserva.status = novo_status
        reserva.save()

        # Cria um registro no histórico para auditoria
        HistoricoStatusReserva.objects.create(
            reserva=reserva,
            status_anterior=status_anterior,
            status_novo=reserva.get_status_display(),
            mudado_por=request.user,
            observacao=f"Status alterado para '{reserva.get_status_display()}' pelo anunciante."
        )

        messages.success(request, f"O status da reserva #{reserva.id} foi alterado com sucesso!")
    
    # Redireciona de volta para a página de detalhes da reserva, independentemente do método.
        return redirect('anunciante_reserva_detail', pk=pk)



# ADICIONE A VIEW ABAIXO:
@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_empreendimento_list(request):
    empreendimentos = Empreendimento.objects.filter(anunciante_responsavel=request.user).order_by('-id')
    return render(request, 'painel/anunciante/anunciante_empreendimento_list.html', {'empreendimentos': empreendimentos})


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_parceiros_list(request):
    empreendimentos_do_anunciante = Empreendimento.objects.filter(anunciante_responsavel=request.user)
    todas_imobiliarias = Imobiliaria.objects.all()
    parcerias_status = {}
    # Otimização: Apenas uma consulta ao banco para todas as parcerias relevantes
    parcerias_existentes = Parceria.objects.filter(empreendimento__in=empreendimentos_do_anunciante).select_related('imobiliaria')
    for parceria in parcerias_existentes:
        # Usamos uma chave composta para lidar com múltiplas parcerias
        parcerias_status[(parceria.imobiliaria.id, parceria.empreendimento.id)] = parceria.get_status_display()
        
    context = {
        'imobiliarias': todas_imobiliarias,
        'parcerias_status': parcerias_status,
        'meus_empreendimentos': empreendimentos_do_anunciante
    }
    return render(request, 'painel/anunciante/anunciante_parceiros_list.html', context)

@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_analytics_view(request):
    return render(request, 'painel/anunciante/anunciante_analytics.html')

@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_configuracoes_view(request):
    return render(request, 'painel/anunciante/anunciante_configuracoes.html')


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_convidar_parceiro(request, imobiliaria_id):
    if request.method == 'POST':
        imobiliaria_a_convidar = get_object_or_404(Imobiliaria, pk=imobiliaria_id)
        empreendimento_id = request.POST.get('empreendimento')
        empreendimento = get_object_or_404(Empreendimento, pk=empreendimento_id, anunciante_responsavel=request.user)

        Parceria.objects.get_or_create(
            empreendimento=empreendimento,
            imobiliaria=imobiliaria_a_convidar
        )
        messages.success(request, f"Convite enviado para {imobiliaria_a_convidar.nome} para o empreendimento {empreendimento.nome}.")

    return redirect('anunciante_parceiros_list')


@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_parcerias_list(request):
    """
    Lista os convites pendentes e as parcerias ativas para a imobiliária do usuário logado.
    """
    imobiliaria_do_usuario = request.user.imobiliaria
    
    convites_pendentes = Parceria.objects.filter(
        imobiliaria=imobiliaria_do_usuario,
        status='pendente'
    ).order_by('-data_convite')
    
    parcerias_ativas = Parceria.objects.filter(
        imobiliaria=imobiliaria_do_usuario,
        status='aceita'
    ).order_by('-data_resposta')
    
    context = {
        'convites_pendentes': convites_pendentes,
        'parcerias_ativas': parcerias_ativas,
    }
    return render(request, 'painel/imobiliaria/imobiliaria_parcerias_list.html', context)


@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_responder_convite(request, parceria_id, resposta):
    """
    Processa a resposta (aceite ou recusa) a um convite de parceria.
    """
    if request.method == 'POST':
        # Garante que o admin só pode responder a convites direcionados à sua imobiliária
        parceria = get_object_or_404(Parceria, pk=parceria_id, imobiliaria=request.user.imobiliaria)
        
        if resposta in ['aceita', 'recusada']:
            parceria.status = resposta
            parceria.data_resposta = timezone.now() # Importar timezone do django.utils
            parceria.save()
            messages.success(request, f"O convite para o empreendimento '{parceria.empreendimento.nome}' foi atualizado.")
    
    return redirect('imobiliaria_parcerias_list')


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_atribuir_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    if lead.unidade_interesse.empreendimento.anunciante_responsavel != request.user:
        messages.error(request, "Você não tem permissão para gerenciar este lead.")
        return redirect('anunciante_lead_list')

    if request.method == 'POST':
        form = AtribuirLeadForm(request.POST, empreendimento=lead.unidade_interesse.empreendimento)
        if form.is_valid():
            corretor_selecionado = form.cleaned_data['corretor']
            lead.corretor_atribuido = corretor_selecionado
            lead.status = 'em_contato'
            lead.save()
            
            # Esta linha agora funciona porque InteracaoLead foi importado
            InteracaoLead.objects.create(
                lead=lead,
                usuario=request.user,
                descricao=f"Lead atribuído ao corretor {corretor_selecionado.get_full_name()}."
            )
            messages.success(request, f"Lead de {lead.nome_cliente} atribuído com sucesso!")
            return redirect('anunciante_lead_list')
    else:
        form = AtribuirLeadForm(empreendimento=lead.unidade_interesse.empreendimento)

    context = {'form': form, 'lead': lead}
    return render(request, 'painel/anunciante/anunciante_atribuir_lead.html', context)



@login_required
@user_passes_test(is_corretor)
def corretor_lead_detail(request, lead_id):
    # Garante que o corretor só pode ver leads que são dele
    lead = get_object_or_404(Lead, pk=lead_id, corretor_atribuido=request.user)
    
    # Formulário para adicionar uma nova interação
    form = InteracaoLeadForm()

    if request.method == 'POST':
        form = InteracaoLeadForm(request.POST)
        if form.is_valid():
            interacao = form.save(commit=False)
            interacao.lead = lead
            interacao.usuario = request.user # O corretor logado é o autor da interação
            interacao.save()
            messages.success(request, "Interação registrada com sucesso!")
            return redirect('corretor_lead_detail', lead_id=lead.id)

    # Pega o histórico de interações para exibir na página
    interacoes = lead.interacoes.all()
    
    context = {
        'lead': lead,
        'interacoes': interacoes,
        'form': form,
    }
    return render(request, 'painel/corretor/corretor_lead_detail.html', context)


@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_equipe_list(request):
    # Pega todos os membros que pertencem à mesma imobiliária do admin logado
    membros = User.objects.filter(imobiliaria=request.user.imobiliaria).exclude(pk=request.user.pk)
    context = {'membros': membros}
    return render(request, 'painel/imobiliaria/imobiliaria_equipe_list.html', context)

@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_membro_create(request):
    if request.method == 'POST':
        form = MembroImobiliariaCreationForm(request.POST)
        if form.is_valid():
            novo_membro = form.save(commit=False)
            novo_membro.imobiliaria = request.user.imobiliaria # Associa à imobiliária do admin
            novo_membro.save()
            messages.success(request, f"Usuário {novo_membro.get_full_name()} criado com sucesso!")
            return redirect('imobiliaria_equipe_list')
    else:
        form = MembroImobiliariaCreationForm()
    
    return render(request, 'painel/imobiliaria/imobiliaria_membro_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_imob)
def imobiliaria_materiais_list(request):
    imobiliaria = request.user.imobiliaria
    materiais = MaterialVenda.objects.filter(imobiliaria=imobiliaria)
    
    if request.method == 'POST':
        form = MaterialVendaForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.imobiliaria = imobiliaria
            material.save()
            messages.success(request, f"Material '{material.titulo}' enviado com sucesso!")
            return redirect('imobiliaria_materiais_list')
    else:
        form = MaterialVendaForm()
        
    context = {
        'materiais': materiais,
        'form': form,
    }
    return render(request, 'painel/imobiliaria/imobiliaria_materiais_list.html', context)


@login_required
@user_passes_test(is_corretor)
def corretor_materiais_list(request):
    # Garante que o corretor só veja materiais da sua própria imobiliária
    if request.user.imobiliaria:
        materiais = MaterialVenda.objects.filter(imobiliaria=request.user.imobiliaria)
    else:
        materiais = [] # Corretores autônomos não têm materiais de imobiliária
    
    context = {'materiais': materiais}
    return render(request, 'painel/corretor/corretor_materiais_list.html', context)


@login_required
@user_passes_test(is_corretor)
def corretor_reserva_detail(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, corretor=request.user)
    return render(request, 'painel/corretor/corretor_reserva_detail.html', {'reserva': reserva})


@login_required
@user_passes_test(is_anunciante_ou_superadmin)
def anunciante_exportar_reservas_csv(request):
    # Define a resposta HTTP como um arquivo CSV para download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_reservas.csv"'
    
    # Cria um "escritor" de CSV que escreve na resposta HTTP
    writer = csv.writer(response)
    
    # Escreve a linha do cabeçalho
    writer.writerow([
        'ID Reserva', 'ID Unidade', 'Empreendimento', 'Cliente', 
        'Email Cliente', 'Corretor', 'Status', 'Data da Criacao'
    ])
    
    # Busca as reservas do anunciante logado
    reservas = Reserva.objects.filter(unidade__empreendimento__anunciante_responsavel=request.user)
    
    # Escreve uma linha para cada reserva
    for reserva in reservas:
        writer.writerow([
            reserva.id,
            reserva.unidade.id,
            reserva.unidade.empreendimento.nome,
            reserva.cliente.get_full_name(),
            reserva.cliente.email,
            reserva.corretor.get_full_name() if reserva.corretor else '-',
            reserva.get_status_display(),
            reserva.data_criacao.strftime('%d/%m/%Y %H:%M')
        ])
        
    return response


@login_required
@user_passes_test(is_gerente_anunciante)
def gerente_anunciante_dashboard(request):
    return render(request, 'painel/gerente_anunciante/dashboard.html')

@login_required
@user_passes_test(is_gerente_anunciante)
def gerente_anunciante_parcerias(request):
    return render(request, 'painel/gerente_anunciante/parcerias.html')

@login_required
@user_passes_test(is_gerente_anunciante)
def gerente_anunciante_leads(request):
    return render(request, 'painel/gerente_anunciante/leads.html')

@login_required
@user_passes_test(is_gerente_anunciante)
def gerente_anunciante_relatorios(request):
    return render(request, 'painel/gerente_anunciante/relatorios.html')


@login_required
@user_passes_test(is_gerente)
def gerente_equipe_list(request):
    return render(request, 'painel/gerente/gerente_equipe_list.html')

@login_required
@user_passes_test(is_gerente)
def gerente_venda_list(request):
    return render(request, 'painel/gerente/gerente_venda_list.html')