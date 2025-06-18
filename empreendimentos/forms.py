# empreendimentos/forms.py (VERSÃO COMPLETA COM TODAS AS IMPORTAÇÕES CORRIGIDAS)

from django import forms
from django.utils.text import slugify

# AQUI ESTÁ A CORREÇÃO PRINCIPAL: Importamos TODOS os modelos que nossos formulários utilizam.
from .models import (
    Empreendimento, 
    Unidade, 
    Amenidade, 
    FiltroLocalizacao, 
    EmpreendimentoFiltro,
    ImagemEmpreendimento, 
    VideoEmpreendimento, 
    DocumentoEmpreendimento
)

from .models import (
    # ... (modelos já importados)
    FluxoPagamento
)
from core.models import User, Imobiliaria
from .models import MaterialVenda


class EmpreendimentoEtapaInicialForm(forms.ModelForm):
    """
    Formulário unificado para a etapa inicial de criação do empreendimento.
    """
    class Meta:
        model = Empreendimento
        fields = [
            'tipo_empreendimento', 'uso', 'nome', 'status_empreendimento', 
            'data_entrega', 'descricao_curta', 'tipo_anunciante', 'nome_anunciante'
        ]
        widgets = {
            'data_entrega': forms.DateInput(attrs={'type': 'date'}),
            'descricao_curta': forms.Textarea(attrs={'rows': 3}),
            'nome_anunciante': forms.TextInput(attrs={'placeholder': 'Ex: Construtora Exemplo S.A.'}),
        }
        labels = {
            'nome': 'Nome do Empreendimento (Este nome será usado para criar a URL)',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.nome)
        
        original_slug = instance.slug
        queryset = Empreendimento.objects.filter(slug=instance.slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        counter = 1
        while queryset.exists():
            instance.slug = f'{original_slug}-{counter}'
            counter += 1
            queryset = Empreendimento.objects.filter(slug=instance.slug)
        
        if commit:
            instance.save()
            # O save_m2m é necessário para campos ManyToMany, como amenidades
            self.save_m2m()
        return instance


class EmpreendimentoEtapa3Form(forms.ModelForm):
    """ Formulário para a Etapa 3: Localização e Contato. """
    class Meta:
        model = Empreendimento
        fields = [ 'cep', 'endereco_completo', 'url_Maps', 'thumbnail_localizacao', 'numero_whatsapp_atendimento' ]
        widgets = {
            'url_Maps': forms.URLInput(attrs={'placeholder': 'Cole aqui a URL completa do Google Maps'}),
            'numero_whatsapp_atendimento': forms.TextInput(attrs={'placeholder': 'Ex: 5511999998888'}),
        }


class EmpreendimentoEtapa6Form(forms.ModelForm):
    """
    Formulário para a Etapa 6, focado em características e amenidades.
    """
    amenidades = forms.ModelMultipleChoiceField(
        # Agora o Python sabe o que é 'Amenidade' pois foi importada
        queryset=Amenidade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Empreendimento
        fields = ['amenidades']


# Formsets
ImagemEmpreendimentoFormSet = forms.inlineformset_factory(
    parent_model=Empreendimento, model=ImagemEmpreendimento, 
    fields=['arquivo', 'legenda', 'ordem'], extra=1, can_delete=True
)

VideoEmpreendimentoFormSet = forms.inlineformset_factory(
    Empreendimento, VideoEmpreendimento, 
    fields=['url_video', 'titulo', 'thumbnail', 'ordem'], extra=1, can_delete=True
)

DocumentoEmpreendimentoFormSet = forms.inlineformset_factory(
    Empreendimento, DocumentoEmpreendimento, 
    fields=['tipo_documento', 'arquivo', 'link_externo'], extra=1, can_delete=True
)

UnidadeFormSet = forms.inlineformset_factory(
    parent_model=Empreendimento, model=Unidade,
    fields=['tipo', 'metragem', 'quartos', 'banheiros', 'vagas', 'valor_total', 'status', 'planta_imagem'],
    extra=5, can_delete=True, min_num=1
)

EmpreendimentoFiltroFormSet = forms.inlineformset_factory(
    parent_model=Empreendimento, model=EmpreendimentoFiltro,
    fields=['filtro', 'valor_numerico', 'unidade_medida', 'texto_complementar'],
    extra=3, can_delete=True
)


class EmpreendimentoEtapa7Form(forms.ModelForm):
    """
    Formulário para as regras de Canais de Venda.
    """
    # Usamos ModelMultipleChoiceField para permitir a seleção de múltiplos corretores/imobiliárias
    corretores_autorizados = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(perfil='corretor'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    imobiliarias_autorizadas = forms.ModelMultipleChoiceField(
        queryset=Imobiliaria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Empreendimento
        fields = [
            'venda_todos_corretores_autonomos',
            'corretores_autorizados',
            'venda_todas_imobiliarias',
            'imobiliarias_autorizadas',
            'visivel_consumidor_final',
            'visivel_para_nao_autorizados'
        ]
        labels = {
            'venda_todos_corretores_autonomos': 'Permitir que TODOS os corretores autônomos da plataforma vendam?',
            'corretores_autorizados': 'Ou selecione corretores autorizados específicos:',
            'venda_todas_imobiliarias': 'Permitir que TODAS as imobiliárias da plataforma vendam?',
            'imobiliarias_autorizadas': 'Ou selecione imobiliárias autorizadas específicas:',
            'visivel_consumidor_final': 'O anúncio será visível para o público geral (clientes finais)?',
            'visivel_para_nao_autorizados': 'Se a venda for restrita, o anúncio deve ser visível para canais não autorizados (apenas para gerar interesse)?'
        }


# Formset para a tabela de fluxo de pagamento
FluxoPagamentoFormSet = forms.inlineformset_factory(
    parent_model=Empreendimento,
    model=FluxoPagamento,
    fields=['serie', 'quantidade', 'valor_unitario'],
    extra=5, # Começa com 5 linhas para a tabela de pagamento
    can_delete=True
)

class EmpreendimentoEtapa8Form(forms.ModelForm):
    """
    Formulário para a Etapa 8 e final: Revisão e Publicação.
    """
    STATUS_CHOICES = [
        ('rascunho', 'Salvar como Rascunho'),
        ('publicado', 'Publicar Anúncio Agora')
    ]
    # Usamos um ChoiceField para o status de publicação, que não está no modelo Empreendimento
    # diretamente, mas será usado na view para atualizar o campo correto.
    status_publicacao = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect,
        label="Status do Anúncio"
    )

    class Meta:
        model = Empreendimento
        fields = ['slug', 'status_publicacao']
        help_texts = {
            'slug': 'Este texto será usado na URL do seu anúncio. Use apenas letras, números e hifens.'
        }


class MaterialVendaForm(forms.ModelForm):
    class Meta:
        model = MaterialVenda
        fields = ['titulo', 'arquivo']        