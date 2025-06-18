from django.contrib.auth.models import AbstractUser
from django.db import models

class Imobiliaria(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=[('ativa', 'Ativa'), ('pendente', 'Pendente'), ('inativa', 'Inativa')], default='pendente')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class User(AbstractUser):
    PERFIS = [
        ('superadmin', 'Super Admin'),
        ('anunciante', 'Anunciante'),
        ('gerente_anunciante', 'Gerente de Anunciante'),
        ('admin_imob', 'Admin de Imobiliária'),
        ('gerente', 'Gerente de Imobiliária'),
        ('corretor', 'Corretor'),
        ('cliente', 'Cliente'),
    ]
    perfil = models.CharField(max_length=20, choices=PERFIS, blank=True)
    imobiliaria = models.ForeignKey(Imobiliaria, on_delete=models.SET_NULL, null=True, blank=True, related_name='membros')
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username