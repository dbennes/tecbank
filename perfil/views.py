from re import X
from django.shortcuts import render
from perfil.models import Perfil

def exibe(request):
     x = Perfil.objects.all()


    


    