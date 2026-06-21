from django.contrib import admin
from .models import Triagem, Atendimento


@admin.register(Triagem)
class TriagemAdmin(admin.ModelAdmin):
    list_display = ('data_triagem', 
                    'peso', 'altura', 
                    'pressao_arterial', 
                    'saturacao', 
                    'sintomas', 
                    'observacoes', 
                    'paciente', 
                    'enfermeiro', 
                    'classificacao_risco')
    list_filter = (
        'classificacao_risco',
        'enfermeiro',
        'data_triagem',
    )

    search_fields = (
        'paciente__nome',
        'enfermeiro__nome',
        'sintomas',
        'observacoes',
    )

    ordering = ('-data_triagem',)

    autocomplete_fields = ('paciente', 'enfermeiro', 'classificacao_risco')


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = (
        'data_hora_inicio',
        'data_hora_fim',
        'diagnostico',
        'prescricao',
        'triagem',
        'get_medicos',
    )

    list_filter = ('triagem', 'medicos')

    ordering = ('-data_hora_inicio',)

    def get_medicos(self, obj):
        return ", ".join([m.nome for m in obj.medicos.all()])

    get_medicos.short_description = 'Médicos'