# reservas/models.py

from django.db import models
from core.models import User
from empreendimentos.models import Unidade, Empreendimento

class Lead(models.Model):
    """Registra um potencial cliente interessado (uma 'solicitação de reserva')."""
    STATUS_LEAD_CHOICES = [
        ('novo', 'Novo'),
        ('em_contato', 'Em Contato'),
        ('qualificado', 'Qualificado'),
        ('desqualificado', 'Desqualificado'),
        ('convertido', 'Convertido'),
    ]
    ORIGEM_LEAD_CHOICES = [
        ('organico', 'Orgânico (Site)'),
        ('link_corretor', 'Link de Corretor'),
        ('manual', 'Criação Manual'),
    ]

    unidade_interesse = models.ForeignKey(Unidade, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')  
    
    # Dados do cliente
    nome_cliente = models.CharField(max_length=255)  
    cpf_cliente = models.CharField(max_length=14, blank=True, null=True)  
    whatsapp_cliente = models.CharField(max_length=15)  
    email_cliente = models.EmailField(blank=True, null=True)  
    
    # Controle e atribuição
    status = models.CharField(max_length=20, choices=STATUS_LEAD_CHOICES, default='novo')  
    origem = models.CharField(max_length=20, choices=ORIGEM_LEAD_CHOICES, default='organico')  
    corretor_atribuido = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads_atribuidos')  
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_interacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead de {self.nome_cliente} para {self.unidade_interesse}"

class InteracaoLead(models.Model):
    """Registra cada contato ou nota sobre um lead."""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interacoes')  
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Usuário que registrou a interação")  
    descricao = models.TextField()  
    data_interacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_interacao']

class Reserva(models.Model):
    """O registro oficial de uma reserva, que bloqueia a unidade."""
    STATUS_RESERVA_CHOICES = [
        ('solicitada', 'Solicitada'),
        ('aprovada', 'Reserva Aceita'),
        ('docs_aguardando', 'Aguardando Documentação'),
        ('docs_aprovados', 'Documentação Aprovada'),
        ('contrato_enviado', 'Contrato Enviado'),
        ('contrato_recebido', 'Contrato Recebido'),
        ('venda_concluida', 'Venda Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    unidade = models.OneToOneField(Unidade, on_delete=models.PROTECT, related_name='reserva')  
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, related_name='compras')  
    corretor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendas_realizadas')  
    
    status = models.CharField(max_length=30, choices=STATUS_RESERVA_CHOICES, default='solicitada')  
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva da Unidade {self.unidade.id} para {self.cliente.get_full_name()}"

class DocumentoReserva(models.Model):
    """Documentos enviados pelo cliente para uma reserva específica."""
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='documentos')  
    arquivo = models.FileField(upload_to='reservas/documentos/')  
    nome_documento = models.CharField(max_length=255)  
    data_upload = models.DateTimeField(auto_now_add=True)  
    uploaded_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  

class HistoricoStatusReserva(models.Model):
    """Log de todas as mudanças de status de uma reserva."""
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='historico_status')  
    status_anterior = models.CharField(max_length=30, null=True, blank=True)  
    status_novo = models.CharField(max_length=30)  
    data_mudanca = models.DateTimeField(auto_now_add=True)  
    mudado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    observacao = models.TextField(blank=True, null=True)  

    class Meta:
        ordering = ['data_mudanca']