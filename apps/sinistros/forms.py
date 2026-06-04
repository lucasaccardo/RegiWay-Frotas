# Funcao: formularios de cadastro, atualizacao de status, anexos e comentarios.
# Responsável: Lucas sureira.

from django import forms
from .models import Sinistro
from apps.core.utils import formatar_placa


class SinistroForm(forms.ModelForm):
    class Meta:
        model = Sinistro
        fields = ['placa', 'chassi', 'cliente', 'telefone_contato', 'data_ocorrencia', 'descricao', 'documento_anexo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: ABC-1234'}),
            'chassi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'telefone_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'data_ocorrencia': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Descreva a avaria ou motivo da manutenção...'}),
            'documento_anexo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_placa(self):
        return formatar_placa(self.cleaned_data.get('placa', ''))
