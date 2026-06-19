from django import forms
from .models import Triagem, Atendimento


class TriagemForm(forms.ModelForm):
    class Meta:
        model = Triagem
        fields = '__all__'

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'