# reservas/forms.py (VERSÃO COMPLETA E CORRIGIDA)

from django import forms
# AQUI ESTÁ A CORREÇÃO: Importamos tanto o Lead quanto a Reserva
from .models import Lead, Reserva

class SolicitarReservaForm(forms.ModelForm):
    """
    Formulário para um cliente visitante solicitar uma reserva, gerando um Lead.
    """
    class Meta:
        model = Lead
        fields = ['nome_cliente', 'whatsapp_cliente', 'email_cliente', 'cpf_cliente']
        widgets = {
            'nome_cliente': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'whatsapp_cliente': forms.TextInput(attrs={'placeholder': 'Seu WhatsApp com DDD'}),
            'email_cliente': forms.EmailInput(attrs={'placeholder': 'Seu melhor e-mail'}),
            'cpf_cliente': forms.TextInput(attrs={'placeholder': 'Seu CPF (opcional)'}),
        }
        labels = {
            'nome_cliente': 'Nome Completo',
            'whatsapp_cliente': 'WhatsApp',
            'email_cliente': 'E-mail',
            'cpf_cliente': 'CPF',
        }

class ReservaDiretaCorretorForm(forms.ModelForm):
    """
    Formulário para o Corretor realizar uma reserva direta em nome de um cliente.
    """
    nome_cliente = forms.CharField(label="Nome Completo do Cliente", max_length=255)
    cpf_cliente = forms.CharField(label="CPF do Cliente", max_length=14)
    email_cliente = forms.EmailField(label="E-mail do Cliente")
    whatsapp_cliente = forms.CharField(label="WhatsApp do Cliente", max_length=15)

    class Meta:
        # O formulário usa o modelo Reserva para validação implícita, mesmo que
        # não estejamos usando campos diretos dele.
        model = Reserva
        fields = ['nome_cliente', 'cpf_cliente', 'email_cliente', 'whatsapp_cliente']