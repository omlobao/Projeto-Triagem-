from django.contrib import admin
from .models import Paciente, Enfermeiro, Medico, ClassificacaoRisco


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display =('nome', 'sobrenome', 'cpf', 'data_nascimento', 'email', 'numero_telefone')
    search_fields = ('nome', 'sobrenome', 'cpf', 'email')
    list_filter = ('data_nascimento',)
    ordering = ('nome', 'sobrenome')

@admin.register(Enfermeiro)
class EnfermeiroAdmin(admin.ModelAdmin):
    list_display =('nome', 'sobrenome', 'cpf', 'coren', 'telefone', 'email')
    search_fields = ('nome', 'sobrenome', 'cpf', 'coren', 'email')
    ordering = ('nome', 'sobrenome')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'cpf', 'CRM', 'telefone', 'especialidade')
    search_fields = ('nome', 'sobrenome', 'cpf', 'CRM', 'email')
    ordering = ('nome', 'sobrenome')

@admin.register(ClassificacaoRisco)
class ClassificacaoRiscoAdmin(admin.ModelAdmin):
    list_display= ('cor', 'prioridade', 'tempo_max_atendimento', 'descricao')
    search_fields =('prioridade', 'descricao')
    ordering = ('cor', 'prioridade')