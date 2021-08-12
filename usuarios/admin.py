from django.contrib import admin
from .models import conta_usuario
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class ListandoUsuarios (admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'agencia', 'conta', 'digito_conta', 'estado', 'pais', 'saldo_brl', 'foto_verificacao_identidade', 'foto_verificacao_usuario', 'email_verificacao' )
    list_display_links = ('nome', 'cpf',)
    search_fields = ('nome', 'cpf', 'agencia', 'conta','estado', 'pais')
    list_filter = ('estado', 'pais', 'foto_verificacao_identidade', 'foto_verificacao_usuario', 'email_verificacao')
    list_editable = ('foto_verificacao_identidade', 'foto_verificacao_usuario', 'email_verificacao')
    list_per_page = 100

  

admin.site.register (conta_usuario, ListandoUsuarios)
