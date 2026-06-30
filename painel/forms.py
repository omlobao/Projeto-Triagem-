from django import forms
from django.contrib.auth.models import User, Group
from cadastro.models import Paciente, Enfermeiro, Medico, ClassificacaoRisco
from .models import ConfiguracaoHospital


# ============================================
# User Forms
# ============================================

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label='Senha',
        min_length=6,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a senha'}),
        label='Confirmar Senha',
    )
    is_staff = forms.BooleanField(
        required=False,
        label='Acesso ao painel administrativo',
        help_text='Permite que o usuário acesse o painel de administração.',
    )
    is_superuser = forms.BooleanField(
        required=False,
        label='Superusuário',
        help_text='Concede todas as permissões automaticamente.',
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Grupos',
        help_text='Segure Ctrl/Cmd para selecionar múltiplos.',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'is_active', 'is_staff', 'is_superuser', 'groups']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Deixe vazio para manter'}),
        label='Nova Senha',
        required=False,
        min_length=6,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a nova senha'}),
        label='Confirmar Nova Senha',
        required=False,
    )
    is_staff = forms.BooleanField(
        required=False,
        label='Acesso ao painel administrativo',
    )
    is_superuser = forms.BooleanField(
        required=False,
        label='Superusuário',
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Grupos',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'is_active', 'is_staff', 'is_superuser', 'groups']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user


# ============================================
# Group Form
# ============================================

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'Nome do Grupo',
            'permissions': 'Permissões',
        }


# ============================================
# Cadastro Forms
# ============================================

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'cpf': 'CPF',
            'data_nascimento': 'Data de Nascimento',
            'numero_telefone': 'Telefone',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_nascimento'].widget = forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            )
            self.initial['data_nascimento'] = (
                self.instance.data_nascimento.strftime('%Y-%m-%d')
                if self.instance.data_nascimento else ''
            )


class EnfermeiroForm(forms.ModelForm):
    class Meta:
        model = Enfermeiro
        fields = '__all__'
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'cpf': 'CPF',
            'coren': 'COREN',
            'telefone': 'Telefone',
            'email': 'E-mail',
        }


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'cpf': 'CPF',
            'CRM': 'CRM',
            'telefone': 'Telefone',
            'especialidade': 'Especialidade',
            'email': 'E-mail',
        }


class ClassificacaoRiscoForm(forms.ModelForm):
    class Meta:
        model = ClassificacaoRisco
        fields = '__all__'
        labels = {
            'cor': 'Cor',
            'prioridade': 'Prioridade',
            'tempo_max_atendimento': 'Tempo Máximo de Atendimento (min)',
            'descricao': 'Descrição',
        }


class ConfiguracaoHospitalForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoHospital
        fields = '__all__'

