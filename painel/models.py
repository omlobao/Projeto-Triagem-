from django.db import models


class ConfiguracaoHospital(models.Model):
    nome_hospital = models.CharField(max_length=100, default='Hospital SENAI', verbose_name='Nome do Hospital')
    subtitulo = models.CharField(
        max_length=200,
        default='Sistema Integrado de Triagem e Atendimento Médico',
        verbose_name='Subtítulo Institucional'
    )
    titulo_documento = models.CharField(max_length=100, default='Receita Médica', verbose_name='Título do Documento')
    subtitulo_documento = models.CharField(
        max_length=100,
        default='Uso Médico e Farmacêutico',
        verbose_name='Subtítulo do Documento'
    )
    local_emissao = models.CharField(max_length=100, default='São Paulo', verbose_name='Cidade / Estado de Emissão')
    rodape_legal = models.CharField(
        max_length=255,
        default='Receita gerada eletronicamente através do Sistema de Triagem Hospitalar SENAI',
        verbose_name='Texto do Rodapé Legal'
    )

    class Meta:
        verbose_name = 'Configuração do Hospital'
        verbose_name_plural = 'Configuração do Hospital'

    def __str__(self):
        return self.nome_hospital

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

