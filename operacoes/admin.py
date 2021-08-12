from django.contrib import admin
from .models import numero_operacao

# Register your models here.

class ListandoOperacoes (admin.ModelAdmin):
    list_display = ('numero_operacao', 'nome_operacao')
    list_display_links = ('numero_operacao', 'nome_operacao')
    search_fields = ('numero_operacao', 'nome_operacao')
    list_filter = ('numero_operacao', 'nome_operacao')
    list_per_page = 50

admin.site.register (numero_operacao, ListandoOperacoes)