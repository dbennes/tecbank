from django.contrib import admin
from .models import Transferencia 

# Register your models here.

class ListandoTransferencias (admin.ModelAdmin):
    list_display = ('numero_operacao', 'operacao', 'nome_usuario', 'cpf_usuario', 'valor_transferido', 'data_transferencia')
    list_display_links = ('numero_operacao', 'operacao')
    search_fields = ('numero_operacao', 'operacao', 'nome_usuario', 'cpf_usuario',)
    list_filter = ('numero_operacao', 'operacao',)
    list_per_page = 100

admin.site.register(Transferencia, ListandoTransferencias)
