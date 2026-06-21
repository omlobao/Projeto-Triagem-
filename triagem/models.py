from django.db import models
from cadastro.models import (
    Paciente,
    Enfermeiro,
    Medico,
    ClassificacaoRisco
)


class Triagem(models.Model):
    data_triagem = models.DateField(auto_now_add=True)
    peso = models.FloatField()
    altura = models.DecimalField(max_digits=4,
                                decimal_places=2)
    pressao_arterial = models.CharField(max_length=20)
    saturacao = models.IntegerField()
    sintomas = models.TextField()
    observacoes = models.TextField(blank=True)
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE
    )
    enfermeiro = models.ForeignKey(Enfermeiro,
                                   on_delete=models.PROTECT)
    classificacao_risco = models.ForeignKey(
        ClassificacaoRisco,
        on_delete=models.PROTECT
    )
    
    def __str__(self):
        return f"Triagem #{self.id} - {self.paciente.nome}"

    @property
    def is_concluida(self):
        return hasattr(self, 'atendimento')


class Atendimento(models.Model):
    data_hora_inicio = models.DateField(auto_now=True)
    data_hora_fim = models.DateTimeField(
        null=True,
        blank=True
    )
    diagnostico = models.TextField()
    prescricao = models.TextField()
    triagem = models.OneToOneField(
        Triagem,
        on_delete=models.CASCADE   
    )
    medicos = models.ManyToManyField(
        Medico
    )

    def __str__(self):
        return f"Atendimento #{self.id}"
