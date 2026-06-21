from django import forms
from django.db import models
from .models import Triagem, Atendimento


from cadastro.models import Paciente

class TriagemForm(forms.ModelForm):
    paciente_novo = forms.BooleanField(required=False, initial=False)
    nome = forms.CharField(max_length=32, required=False)
    sobrenome = forms.CharField(max_length=32, required=False)
    cpf = forms.CharField(max_length=15, required=False)
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    numero_telefone = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Triagem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].required = False
        
        # Oculta label do paciente original
        if 'paciente' in self.fields:
            self.fields['paciente'].label = ''

    def clean(self):
        cleaned_data = super().clean()
        paciente_novo = cleaned_data.get('paciente_novo')
        paciente = cleaned_data.get('paciente')

        if paciente_novo:
            required_fields = ['nome', 'sobrenome', 'cpf', 'data_nascimento', 'numero_telefone', 'email']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'Este campo é obrigatório para um novo paciente.')
            
            cpf = cleaned_data.get('cpf')
            if cpf and Paciente.objects.filter(cpf=cpf).exists():
                self.add_error('cpf', 'Um paciente com este CPF já está cadastrado.')
        else:
            if not paciente:
                self.add_error('paciente', 'Selecione um paciente existente ou cadastre um novo.')
        
        return cleaned_data

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra as triagens para mostrar apenas aquelas que ainda NÃO possuem atendimento
        if self.instance and self.instance.pk:
            # Se for edição, mostra as que não tem atendimento + a triagem atual
            self.fields['triagem'].queryset = Triagem.objects.filter(
                models.Q(atendimento__isnull=True) | models.Q(id=self.instance.triagem_id)
            )
        else:
            # Se for criação, mostra apenas as que não tem atendimento
            self.fields['triagem'].queryset = Triagem.objects.filter(atendimento__isnull=True)