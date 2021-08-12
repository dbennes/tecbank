from django.contrib import admin
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'
    list_display = ( 'cpf', )

class ListandoUsuarios (admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'agencia', 'conta', 'digito_conta', 'estado', 'pais', 'saldo_brl', 'foto_verificacao_identidade', 'foto_verificacao_usuario', 'email_verificacao')
    list_display_links = ('nome', 'cpf',)
    search_fields = ( 'nome', 'cpf', 'agencia', 'conta','estado', 'pais' )
    list_filter = ('estado', 'pais', 'foto_verificacao_identidade', 'foto_verificacao_usuario', 'email_verificacao')
    list_editable = ('foto_verificacao_identidade', 'foto_verificacao_usuario', 'email_verificacao')
    list_per_page = 100
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline, )
    ListandoUsuarios = (ListandoUsuarios, )
    

admin.site.register(Perfil, ListandoUsuarios)

