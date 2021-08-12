from django.db import models
from datetime import datetime

from django.db.models.deletion import CASCADE
from usuarios.models import conta_usuario
from operacoes.models import numero_operacao

from django.contrib.auth.models import User

class Transferencia(models.Model):

    nome_usuario = models.ForeignKey(User, on_delete=models.CASCADE)    
    numero_operacao = models.IntegerField()
    operacao = models.CharField(max_length=200)

    cpf_usuario = models.CharField(max_length=200)
    conta_usuario = models.IntegerField()
    digito_conta_usuario = models.IntegerField()
    agencia_usuario = models.IntegerField()

    nome_favorecido = models.CharField(max_length=200)
    cpf_favorecido = models.CharField(max_length=200)
    agencia_favorecido = models.CharField(max_length=200)
    conta_favorecido = models.IntegerField()
    digito_conta_favorecido = models.IntegerField()
    banco_favorecido = models.CharField(max_length=200)
    banco_numero = models.CharField(max_length=200)
    
    valor_transferido = models.DecimalField(max_digits=6, decimal_places=2)
    data_transferencia = models.DateTimeField(default=datetime.now, blank=True)
