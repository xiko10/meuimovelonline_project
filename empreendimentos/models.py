from django.db import models
from core.models import User, Imobiliaria # Importamos nossos modelos do app core

class Empreendimento(models.Model):
    """Modelo central que representa um empreendimento imobiliário."""
    TIPO_EMPREENDIMENTO_CHOICES = [('vertical', 'Vertical'), ('horizontal', 'Horizontal'), ('loteamento', 'Loteamento')]
    TIPO_USO_CHOICES = [('residencial', 'Residencial'), ('comercial', 'Comercial'), ('misto', 'Misto')]
    STATUS_EMPREENDIMENTO_CHOICES = [('breve_lancamento', 'Breve Lançamento'), ('lancamento', 'Lançamento'), ('em_obras', 'Em Obras'), ('pronto', 'Pronto para morar')]
    
    # Informações Básicas
    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL amigável, ex: 'meu-empreendimento-incrivel'")
    tipo_empreendimento = models.CharField(max_length=20, choices=TIPO_EMPREENDIMENTO_CHOICES)
    uso = models.CharField(max_length=20, choices=TIPO_USO_CHOICES)
    status_empreendimento = models.CharField(max_length=20, choices=STATUS_EMPREENDIMENTO_CHOICES)
    data_entrega = models.DateField(null=True, blank=True)
    descricao_curta = models.CharField(max_length=300, help_text="Um resumo atrativo do empreendimento.")

    # Informações do Anunciante (snapshot no momento do cadastro)
    tipo_anunciante = models.CharField(max_length=50, help_text="Construtora, Incorporadora, etc.")
    nome_anunciante = models.CharField(max_length=255)
    descricao_anunciante = models.TextField(max_length=500, blank=True)
    
    # Localização e Contato
    cep = models.CharField(max_length=9)
    endereco_completo = models.CharField(max_length=512)
    url_Maps = models.URLField(max_length=2048, help_text="Link para o mapa embedado.")
    thumbnail_localizacao = models.ImageField(upload_to='empreendimentos/thumbnails_mapa/')
    numero_whatsapp_atendimento = models.CharField(max_length=15)
    
    # Relação com o dono do anúncio
    anunciante_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empreendimentos')
    
    # Regras de Venda
    limite_reservas_canal = models.PositiveIntegerField(null=True, blank=True, help_text="Nº máx. de reservas ativas por corretor/imobiliária")
    
    def __str__(self):
        return self.nome

class Amenidade(models.Model):
    """Amenidades cadastráveis (Academia, Piscina, etc.)."""
    nome = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Nome do ícone de uma biblioteca como Material Icons")
    empreendimentos = models.ManyToManyField(Empreendimento, related_name='amenidades', blank=True)

    def __str__(self):
        return self.nome

class Unidade(models.Model):
    """Representa uma unidade individual dentro de um empreendimento."""
    TIPO_UNIDADE_CHOICES = [('apartamento', 'Apartamento'), ('studio', 'Studio'), ('cobertura', 'Cobertura'), ('lote', 'Lote'), ('sala', 'Sala')]
    STATUS_UNIDADE_CHOICES = [('disponivel', 'Disponível'), ('reservada', 'Reservada'), ('vendida', 'Vendida'), ('indisponivel', 'Indisponível')]

    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='unidades')
    tipo = models.CharField(max_length=50, choices=TIPO_UNIDADE_CHOICES)
    metragem = models.DecimalField(max_digits=8, decimal_places=2)
    quartos = models.PositiveIntegerField(default=0)
    banheiros = models.PositiveIntegerField(default=0)
    vagas = models.PositiveIntegerField(default=0)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_UNIDADE_CHOICES, default='disponivel')
    planta_imagem = models.ImageField(upload_to='unidades/plantas/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.empreendimento.nome} - Unidade {self.id}"

class ImagemEmpreendimento(models.Model):
    """Armazena as imagens da galeria principal do empreendimento."""
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='imagens_galeria') 
    arquivo = models.ImageField(upload_to='empreendimentos/galeria/') 
    legenda = models.CharField(max_length=255, blank=True) 
    ordem = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['ordem'] 

    def __str__(self):
        return f"Imagem de {self.empreendimento.nome} - Ordem {self.ordem}" 

class VideoEmpreendimento(models.Model):
    """Armazena os vídeos associados ao empreendimento."""
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='videos') 
    url_video = models.URLField(max_length=2048, help_text="URL do vídeo (ex: YouTube, Vimeo)") 
    titulo = models.CharField(max_length=255, blank=True) 
    thumbnail = models.ImageField(upload_to='empreendimentos/thumbnails_video/')
    ordem = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['ordem'] 

    def __str__(self):
        return f"Vídeo '{self.titulo}' de {self.empreendimento.nome}" 

class DocumentoEmpreendimento(models.Model):
    """Armazena documentos como Memorial Descritivo, Contrato Padrão, etc."""
    TIPO_DOCUMENTO_CHOICES = [
        ('revista', 'Revista Digital'),
        ('ficha', 'Ficha Técnica'),
        ('memorial', 'Memorial Descritivo'),
        ('contrato', 'Contrato Padrão'),
        ('tour_virtual', 'Tour Virtual'),
    ]
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    arquivo = models.FileField(upload_to='empreendimentos/documentos/', null=True, blank=True, help_text="Para upload de arquivos PDF, JPG, etc.")
    link_externo = models.URLField(max_length=2048, null=True, blank=True, help_text="Para links externos como o do Tour Virtual.")

    def __str__(self):
        return f"{self.get_tipo_documento_display()} de {self.empreendimento.nome}"