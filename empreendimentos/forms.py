# empreendimentos/forms.py

from django import forms
from django.utils.text import slugify
from .models import Empreendimento, Unidade, ImagemEmpreendimento, VideoEmpreendimento, DocumentoEmpreendimento

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
        queryset = Empreendimento.objects.all().filter(slug=instance.slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        counter = 1
        while queryset.exists():
            instance.slug = f'{original_slug}-{counter}'
            counter += 1
            queryset = Empreendimento.objects.all().filter(slug=instance.slug)
        
        if commit:
            instance.save()
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

# Formsets para a Etapa 4
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