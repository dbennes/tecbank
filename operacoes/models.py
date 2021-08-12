from django.db import models

class numero_operacao (models.Model):

    numero_operacao = models.IntegerField()
    nome_operacao = models.CharField(max_length=200)

    def __str__(self):
        return self.nome_operacao