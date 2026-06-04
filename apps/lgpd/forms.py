# Funcao: formularios de aceite, consulta, exclusao, anonimizacao e portabilidade.
# Responsável: Lucas sureira, Pacheco.

from django import forms
from django.contrib.auth.models import User

class AtualizarDadosForm(forms.ModelForm):
    """
    Formulário para o usuário atualizar seus próprios dados pessoais.
    Vinculado diretamente ao modelo de Usuário padrão do Django.
    """
    class Meta:
        model = User
        # Definimos quais campos o usuário tem permissão para alterar
        fields = ['first_name', 'last_name', 'email']
        
        # Colocamos as classes CSS para o front-end estilizar depois
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail corporativo'}),
        }
