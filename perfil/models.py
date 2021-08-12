from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, blank=True)
    cpf = models.CharField(max_length=200, blank=True)
    identidade = models.CharField(max_length=200, blank=True)

    agencia = models.CharField(max_length=200, blank=True)
    conta = models.CharField(max_length=200, blank=True)
    digito_conta = models.CharField(max_length=200, blank=True)

    email = models.CharField(max_length=200, blank=True)
    numero_celular = models.CharField(max_length=200,  blank=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=200, blank=True, null=True)
    pais = models.CharField(max_length=200, blank=True, null=True)

    saldo_brl = models.DecimalField (max_digits=12, decimal_places=2, null=True)

    #Para verificações futuras
    foto_verificacao_identidade = models.BooleanField(default=False)
    foto_verificacao_usuario = models.BooleanField(default=False)
    email_verificacao = models.BooleanField(default=False)

    foto_identidade = models.ImageField(upload_to='foto_identidade/%d/%m/%Y', blank=True)
    foto_usuario = models.ImageField(upload_to='foto_usuario/%d/%m/%Y', blank=True)

#ESSA PARTE DO CODIGO INSERE DADOS AO CRIAR UM USUARIO 
#AUTOMATICAMENTE NA TABELA PERFIL COM RELACIONAMENTO DA TABELA USER

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    instance.perfil.save()
