from django.shortcuts import render
from .models import Transferencia

def index(request):
  
  
    transferencias = Transferencia.objects.all()

    dados = {
        'transferencias' : transferencias
    }


    return render(request, 'index.html', dados )

def sobre (request):
    return render (request, 'sobre.html')    

def meuperfil (request):
    return render (request, 'meuperfil.html')
