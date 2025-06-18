from django import forms
from .models import Lead, Reserva, InteracaoLead, DocumentoReserva 
from core.models import User

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


class AtribuirLeadForm(forms.Form):
    """
    Formulário para o Anunciante selecionar um corretor para atribuir um lead.
    """
    corretor = forms.ModelChoiceField(
        queryset=User.objects.none(), # O queryset será preenchido dinamicamente na view
        label="Selecione o Corretor",
        required=True
    )

    def __init__(self, *args, **kwargs):
        # Removemos o empreendimento do kwargs para passar para o super()
        empreendimento = kwargs.pop('empreendimento', None)
        super().__init__(*args, **kwargs)

        if empreendimento:
            # Lógica para encontrar corretores de imobiliárias parceiras
            imobiliarias_parceiras_ids = empreendimento.parcerias.filter(status='aceita').values_list('imobiliaria_id', flat=True)
            
            # Filtra os usuários que são corretores E pertencem a uma das imobiliárias parceiras
            self.fields['corretor'].queryset = User.objects.filter(
                perfil='corretor',
                imobiliaria__id__in=imobiliarias_parceiras_ids
            )


class InteracaoLeadForm(forms.ModelForm):
    """
    Formulário para o corretor registrar uma nova interação com um lead.
    """
    class Meta:
        model = InteracaoLead
        fields = ['descricao'] # Apenas o campo de descrição será preenchido pelo usuário
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva a interação. Ex: Cliente informado sobre o fluxo de pagamento.'})
        }
        labels = {
            'descricao': 'Registrar Nova Interação'
        }


class DocumentoReservaUploadForm(forms.ModelForm):
    """
    Formulário para fazer o upload de um documento para uma reserva específica.
    """
    class Meta:
        model = DocumentoReserva
        fields = ['nome_documento', 'arquivo']
        labels = {
            'nome_documento': 'Nome do Documento (ex: RG, CPF, Comprovante de Renda)',
            'arquivo': 'Selecione o arquivo'
        }
