# empreendimentos/models.py (VERSÃO COMPLETA E FINAL)

from django.db import models
from core.models import User, Imobiliaria

class Empreendimento(models.Model):
    TIPO_EMPREENDIMENTO_CHOICES = [('vertical', 'Vertical'), ('horizontal', 'Horizontal'), ('loteamento', 'Loteamento')]
    TIPO_USO_CHOICES = [('residencial', 'Residencial'), ('comercial', 'Comercial'), ('misto', 'Misto')]
    STATUS_EMPREENDIMENTO_CHOICES = [('breve_lancamento', 'Breve Lançamento'), ('lancamento', 'Lançamento'), ('em_obras', 'Em Obras'), ('pronto', 'Pronto para morar')]
    STATUS_PUBLICACAO_CHOICES = [('rascunho', 'Rascunho'), ('publicado', 'Publicado')] # Para a Etapa 8
    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL amigável, ex: 'meu-empreendimento-incrivel'")
    tipo_empreendimento = models.CharField(max_length=20, choices=TIPO_EMPREENDIMENTO_CHOICES)
    uso = models.CharField(max_length=20, choices=TIPO_USO_CHOICES)
    status_empreendimento = models.CharField(max_length=20, choices=STATUS_EMPREENDIMENTO_CHOICES)
    data_entrega = models.DateField(null=True, blank=True)
    descricao_curta = models.CharField(max_length=300, help_text="Um resumo atrativo do empreendimento.")
    tipo_anunciante = models.CharField(max_length=50, help_text="Construtora, Incorporadora, etc.")
    nome_anunciante = models.CharField(max_length=255)
    descricao_anunciante = models.TextField(max_length=500, blank=True)
    cep = models.CharField(max_length=9)
    endereco_completo = models.CharField(max_length=512)
    url_Maps = models.URLField(max_length=2048, help_text="Link para o mapa embedado.")
    thumbnail_localizacao = models.ImageField(upload_to='empreendimentos/thumbnails_mapa/')
    numero_whatsapp_atendimento = models.CharField(max_length=15)
    anunciante_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empreendimentos')
    limite_reservas_canal = models.PositiveIntegerField(null=True, blank=True, help_text="Nº máx. de reservas ativas por corretor/imobiliária")
    venda_todos_corretores_autonomos = models.BooleanField(default=False)
    corretores_autorizados = models.ManyToManyField(User, related_name='empreendimentos_autorizados_corretor', blank=True)
    venda_todas_imobiliarias = models.BooleanField(default=False)
    imobiliarias_autorizadas = models.ManyToManyField(Imobiliaria, related_name='empreendimentos_autorizados_imob', blank=True)
    visivel_consumidor_final = models.BooleanField(default=True)
    visivel_para_nao_autorizados = models.BooleanField(default=True)
    status_publicacao = models.CharField(max_length=20, choices=STATUS_PUBLICACAO_CHOICES, default='rascunho')
    def __str__(self):
        return self.nome

# --- ADICIONE AS CLASSES ABAIXO NO SEU ARQUIVO ---

class FiltroLocalizacao(models.Model):
    """ Contém os tipos de filtros de proximidade. Ex: 'Próximo a Metrô' """
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class EmpreendimentoFiltro(models.Model):
    """ Tabela intermediária que liga um Empreendimento a um Filtro, com dados extras. """
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE)
    filtro = models.ForeignKey(FiltroLocalizacao, on_delete=models.CASCADE)
    valor_numerico = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Ex: 500")
    unidade_medida = models.CharField(max_length=10, choices=[('m', 'metros'), ('km', 'km')], null=True, blank=True)
    texto_complementar = models.CharField(max_length=50, blank=True, help_text="Ex: 'Estação Tatuapé'")
    class Meta:
        unique_together = ('empreendimento', 'filtro')

class ProgramaHabitacional(models.Model):
    """ Contém os tipos de programas. Ex: 'Minha Casa Minha Vida' """
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class EmpreendimentoProgramaHabitacional(models.Model):
    """ Liga um Empreendimento a um Programa Habitacional. """
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE)
    programa = models.ForeignKey(ProgramaHabitacional, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('empreendimento', 'programa')

# --- As classes abaixo já devem existir no seu arquivo, confirme que estão iguais ---

class Amenidade(models.Model):
    # ... (código existente)
    nome = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Nome do ícone de uma biblioteca como Material Icons")
    empreendimentos = models.ManyToManyField(Empreendimento, related_name='amenidades', blank=True)
    def __str__(self):
        return self.nome

class Unidade(models.Model):
    # ... (código existente)
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
    # ... (código existente)
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='imagens_galeria')
    arquivo = models.ImageField(upload_to='empreendimentos/galeria/')
    legenda = models.CharField(max_length=255, blank=True)
    ordem = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['ordem']
    def __str__(self):
        return f"Imagem de {self.empreendimento.nome} - Ordem {self.ordem}"

class VideoEmpreendimento(models.Model):
    # ... (código existente)
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
    # ... (código existente)
    TIPO_DOCUMENTO_CHOICES = [('revista', 'Revista Digital'), ('ficha', 'Ficha Técnica'), ('memorial', 'Memorial Descritivo'), ('contrato', 'Contrato Padrão'), ('tour_virtual', 'Tour Virtual')]
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    arquivo = models.FileField(upload_to='empreendimentos/documentos/', null=True, blank=True, help_text="Para upload de arquivos PDF, JPG, etc.")
    link_externo = models.URLField(max_length=2048, null=True, blank=True, help_text="Para links externos como o do Tour Virtual.")
    def __str__(self):
        return f"{self.get_tipo_documento_display()} de {self.empreendimento.nome}"
    
class FluxoPagamento(models.Model):
    """
    Representa uma linha da tabela de fluxo de pagamento de um empreendimento.
    """
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='fluxo_pagamento')
    serie = models.CharField(max_length=100, help_text="Ex: 'Ato', '30 dias', '60 dias', 'Anual 2025'")
    quantidade = models.PositiveIntegerField(help_text="Número de parcelas nesta série")
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2, help_text="Valor de cada parcela")
    
    def __str__(self):
        return f"{self.empreendimento.nome} - {self.serie}"
    

class Parceria(models.Model):
    STATUS_PARCERIA_CHOICES = [('pendente', 'Pendente'), ('aceita', 'Aceita'), ('recusada', 'Recusada'), ('revogada', 'Revogada')]
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE, related_name='parcerias')
    imobiliaria = models.ForeignKey(Imobiliaria, on_delete=models.CASCADE, related_name='parcerias')
    status = models.CharField(max_length=20, choices=STATUS_PARCERIA_CHOICES, default='pendente')
    data_convite = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ('empreendimento', 'imobiliaria')
    def __str__(self):
        return f"Parceria entre {self.empreendimento.nome} e {self.imobiliaria.nome}"
    
class MaterialVenda(models.Model):
    """
    Armazena um arquivo de material de venda (PDF, Tabela, etc.)
    associado a uma imobiliária.
    """
    imobiliaria = models.ForeignKey(Imobiliaria, on_delete=models.CASCADE, related_name='materiais')
    titulo = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to='materiais_venda/')
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Material de Venda"
        verbose_name_plural = "Materiais de Venda"
        ordering = ['-data_upload']

    def __str__(self):
        return self.titulo


