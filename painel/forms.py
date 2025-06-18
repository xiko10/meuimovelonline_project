# painel/forms.py

from django import forms
from core.models import User

class MembroImobiliariaCreationForm(forms.ModelForm):
    """
    Formulário para o Admin de Imobiliária criar novos membros (Corretores ou Gerentes).
    """
    PERFIS_IMOBILIARIA = [
        ('corretor', 'Corretor'),
        ('gerente', 'Gerente de Imobiliária'),
    ]
    
    perfil = forms.ChoiceField(choices=PERFIS_IMOBILIARIA, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'perfil']
    
    def save(self, commit=True):
        # Sobrescreve o save para lidar com a senha e outros campos
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user