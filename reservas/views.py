# reservas/views.py (VERSÃO COMPLETA E CORRIGIDA)

# 1. Importações do Django
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test # user_passes_test importado corretamente

# 2. Importações dos nossos apps
from .forms import SolicitarReservaForm, ReservaDiretaCorretorForm
from .models import Lead, Reserva, HistoricoStatusReserva # Reserva e HistoricoStatusReserva importados
from empreendimentos.models import Unidade
from core.models import User
from core.decorators import is_corretor # Decorator de perfil importado

# -----------------------------------------------------------------------------

def solicitar_reserva_view(request, unidade_id):
    """
    Processa o formulário de solicitação de reserva enviado pelo visitante.
    """
    unidade = get_object_or_404(Unidade, pk=unidade_id)

    if request.method == 'POST':
        form = SolicitarReservaForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.unidade_interesse = unidade
            lead.save()
            
            messages.success(request, 'Sua solicitação foi enviada com sucesso! Em breve um de nossos corretores entrará em contato.')
            
            return redirect('empreendimentos:detail', slug=unidade.empreendimento.slug)
    
    return redirect('empreendimentos:detail', slug=unidade.empreendimento.slug)


@login_required
@user_passes_test(is_corretor) # Nome do decorator corrigido
def reserva_direta_corretor_view(request, unidade_id):
    """
    Processa a reserva direta feita por um Corretor.
    """
    unidade = get_object_or_404(Unidade, pk=unidade_id)

    if unidade.status != 'disponivel':
        messages.error(request, 'Esta unidade não está mais disponível para reserva.')
        return redirect('empreendimentos:detail', slug=unidade.empreendimento.slug)

    if request.method == 'POST':
        form = ReservaDiretaCorretorForm(request.POST)
        if form.is_valid():
            cliente_email = form.cleaned_data['email_cliente']
            
            cliente, created = User.objects.get_or_create(
                email=cliente_email,
                defaults={
                    'username': cliente_email,
                    'first_name': form.cleaned_data['nome_cliente'].split(' ')[0],
                    'last_name': ' '.join(form.cleaned_data['nome_cliente'].split(' ')[1:]),
                    'cpf': form.cleaned_data['cpf_cliente'],
                    'whatsapp': form.cleaned_data['whatsapp_cliente'],
                    'perfil': 'cliente'
                }
            )
            if created:
                cliente.set_unusable_password() 
                cliente.save()

            unidade.status = 'reservada'
            unidade.save()

            reserva = Reserva.objects.create(
                unidade=unidade,
                cliente=cliente,
                corretor=request.user,
                status='aprovada'
            )
            
            HistoricoStatusReserva.objects.create(
                reserva=reserva,
                status_novo=reserva.status,
                mudado_por=request.user,
                observacao='Reserva direta realizada pelo corretor.'
            )

            messages.success(request, f'Unidade {unidade.id} reservada com sucesso para {cliente.get_full_name()}!')
            return redirect('empreendimentos:detail', slug=unidade.empreendimento.slug)
    
    # Se for um GET, redireciona, pois esta URL só processa POST.
    return redirect('empreendimentos:detail', slug=unidade.empreendimento.slug)