# pyrefly: ignore [missing-import]
from django.db import models



class Paciente(models.Model):
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=32)
    cpf = models.CharField(max_length=15,
                            unique=True,
                            db_index=True)
    data_nascimento = models.DateField()
    numero_telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    def telefone_completo(self):
        return f"({self.ddd_telefone}) {self.numero_telefone}"
    

class Enfermeiro(models.Model):
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=15,
                           unique=True,
                           db_index=True)
    coren = models.CharField(max_length=20,
                             unique=True)
    telefone = models.TextField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


class Medico(models.Model):
    nome = models.CharField(max_length=32)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=15,
                           unique=True,
                           db_index=True)
    CRM = models.CharField(max_length=6,
                           unique=True)
    telefone = models.CharField(max_length=15)
    especialidade = models.TextField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    

class ClassificacaoRisco(models.Model):
    cor = models.CharField(max_length=20)
    prioridade = models.CharField(max_length=20)
    tempo_max_atendimento = models.IntegerField()
    descricao = models.TextField()

    def __str__(self):
        return f"{self.cor} {self.descricao}"