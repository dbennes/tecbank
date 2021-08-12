from django.db import models
from django.db.models.fields import IntegerField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class conta_usuario (models.Model):

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=200)
    identidade = models.CharField(max_length=200)

    agencia = models.IntegerField()
    conta = models.IntegerField()
    digito_conta = models.IntegerField()

    email = models.CharField(max_length=200)
    numero_celular = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)

    saldo_brl = models.DecimalField (max_digits=6, decimal_places=2)

    #Para verificações futuras
    foto_verificacao_identidade = models.BooleanField(default=False)
    foto_verificacao_usuario = models.BooleanField(default=False)
    email_verificacao = models.BooleanField(default=False)

    foto_identidade = models.ImageField(upload_to='foto_identidade/%d/%m/%Y', blank=True)
    foto_usuario = models.ImageField(upload_to='foto_usuario/%d/%m/%Y', blank=True)
        

    def __str__(self):
        return self.nome