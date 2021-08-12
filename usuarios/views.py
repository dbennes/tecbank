from django.core import paginator
from perfil.models import Perfil
from django.shortcuts import redirect, render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from conta_corrente.models import Transferencia
from usuarios.models import conta_usuario
from random import randint
import re
import decimal
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from perfil.models import Perfil

# Create your views here.
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmacao_senha = request.POST ['confirmacao_senha']
        cpf = request.POST['CPF']
        rg = request.POST['RG']
        numero_celular =  request.POST['numero_celular']

    #VERIFICA SE NOS FORMULARIOS EXISTEM ESPAÇO EM BRANCO

        if campo_vazio(nome):
            messages.error(request, 'O campo não pode ficar em branco!')
            return redirect ('cadastro')

        if campo_vazio (email):
            messages.error(request, 'O campo não pode ficar em branco!')
            return redirect ('cadastro')

        if campo_vazio (cpf):
            messages.error(request, 'O campo não pode ficar em branco!')
            return redirect ('cadastro')

        if campo_vazio (rg):
            messages.error(request, 'O campo não pode ficar em branco!')
            return redirect ('cadastro')

        if campo_vazio (numero_celular):
            messages.error(request, 'O campo N° Celular não pode ficar em branco!')
            return redirect ('cadastro')

    #VERIFICAÇÃO DE SENHA

        if validacao_senhas (senha, confirmacao_senha):
            messages.error(request, 'As senhas não conferem!')
            return redirect ('cadastro')

    #VERIFICAÇÃO SE USUARIO JÁ EXISTE

        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado!')
            return redirect ('cadastro')
        
        if User.objects.filter(username=cpf).exists():
            messages.error(request, 'Nome usuário já cadastrado!')
            return redirect ('cadastro')
        
    #registra novo usuario na TABELA USER padrao do django
        user = User.objects.create_user(
            username=cpf, 
            email=email, 
            password=senha,
            first_name=nome,
            last_name=sobrenome,
        )
        user.save()

    #Salva na TABELA PERFIL
        user.perfil.nome = nome + " " + sobrenome
        user.perfil.cpf = cpf
        user.perfil.email = email
        user.perfil.identidade = rg
        user.perfil.numero_celular = numero_celular

    #Agencia
        user.perfil.agencia = "0001"

    #SALDO 0.00
        user.perfil.saldo_brl = 0.00
    
    #DIGITO 
        user.perfil.digito_conta = randint (1, 9)

    # CRIAÇAO DA CONTA COM VALIDAÇÕES
        conta = randint (10100, 99999)

        if re.findall(r'(\d)\1+', str(conta)):

             while re.findall(r'(\d)\1+', str(conta)):
                conta2 = randint (10100, 99999)

                if re.findall(r'(\d)\1+', str(conta2)): 
                    pass
                elif Perfil.objects.filter(conta=conta2).exists():
                    pass
                else:    
                    user.perfil.conta = conta2
                    break    
        else:

            if Perfil.objects.filter(conta=conta).exists():

                while Perfil.objects.filter(conta=conta).exists():  
                    conta2 = randint (10100, 99999)

                    if re.findall(r'(\d)\1+', str(conta)): 
                        pass
                    elif Perfil.objects.filter(conta=conta2).exists():
                        pass
                    else:    
                        user.perfil.conta = conta2
                        break
            else:
                user.perfil.conta = conta
                
        user.save()
          
        messages.success(request, 'Usuario cadastrado com sucesso!')
        print('Usuario cadastrado com sucesso')
        return redirect ('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            senha = request.POST['senha']

            if campo_vazio(email) == "" or campo_vazio(senha) == "":
                messages.error(request, 'Usuário e senha não podem ficar em branco!')

            if User.objects.filter(email=email).exists():
                nome = User.objects.filter(email=email).values_list('username', flat=True).get()
                user = auth.authenticate(request, username=nome, password=senha)

                teste = User.objects.filter(email=email).exists()
                print (teste)

                if user is not None:
                    auth.login(request, user)
                    messages.success(request, 'Login realizado com sucesso!') 

                return redirect ('dashboard')

            if not User.objects.filter(email=email).exists():
                messages.error(request, 'E-mail não cadastrado!')

    return render (request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')
    

def dashboard(request):
    if request.user.is_authenticated:
        id_usuario = request.user.id
        transferencias = Transferencia.objects.filter(nome_usuario=id_usuario).order_by('-data_transferencia')
        dados_perfil = Perfil.objects.filter(user_id=id_usuario)

        #Aqui leio o json na pasta e retorno para a view dashboard e exibo em um FOR \o\
        with open ('techbank_app/static/assets/json/lista_bancos.json', 'r', encoding='utf8') as f:
            lista_bancos = json.load(f)

        dados = {
            'transferencias' : transferencias,
            'dados_perfil' : dados_perfil,
            'lista_bancos' : lista_bancos
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('login')

def perfil(request):
    if request.user.is_authenticated:
        id_usuario = request.user.id
        transferencias = Transferencia.objects.filter(nome_usuario=id_usuario)
        dados_perfil = Perfil.objects.filter(user_id=id_usuario)

        dados = {
            'transferencias' : transferencias,
            'dados_perfil' : dados_perfil
        }

        return render(request, 'usuarios/perfil.html', dados)
    else:
        return redirect('login')


def transferencia (request):

    if request.method == 'POST':
        numero_operacao = request.POST['numero_operacao']
        banco_favorecido = request.POST['banco_favorecido']
        cpf_favorecido = request.POST['cpf_favorecido']
        valor_transferido = request.POST['valor_brl']
        nome_favorecido = request.POST['nome_favorecido']
        agencia_favorecido = request.POST['agencia_favorecido']
        conta_favorecido = request.POST['conta_favorecido']
        digito_conta_favorecido = request.POST['digito_conta_favorecido']

        #formato decimal para inserir no banco
        valor1 = valor_transferido.replace('.','')  
        valor_formatado = valor1.replace(',','.')

        valor_transferencia = float(valor_formatado)

        id_usuario = get_object_or_404(User, pk=request.user.id)

        #Aqui faço um select geral
        saldo_objeto = Perfil.objects.values().get(user_id = id_usuario)

        #Trato os dados que vem do select dentro de um discionario e exibo separadamente
        saldo = saldo_objeto['saldo_brl']

        cpf = saldo_objeto['cpf']
        conta = saldo_objeto['conta']
        digito_conta = saldo_objeto['digito_conta']
        agencia = saldo_objeto['agencia']   

        if saldo >= valor_transferencia:

            if valor_transferencia <= 4.99:
                messages.error(request, 'Valor minimo de transferência é acima de R$ 5,00')
                
            elif valor_transferencia >= 10000:
                messages.error(request, 'Valor máximo de transferência é de R$ 10.000,00')

            else:
                #NESSA CONDIÇÃO IF VERIFICO SE A TRANSFERENCIA É ENTRE NOSSAS CONTAS OU NAO
                nosso_banco = "9999"

                if banco_favorecido == nosso_banco:

                    if Perfil.objects.filter(cpf=cpf_favorecido).exists():

                        #NESSA CONDIÇÃO IF VERIFICO SE EXISTEM CPF CADASTRADOS COM O QUE  FOI PASSADO NO INPUT

                        #Aqui faço um select geral
                        informacoes_favorecido = Perfil.objects.values().get(cpf = cpf_favorecido)

                        #Trato os dados que vem do select dentro de um discionario e exibo separadamente
                        saldo_favorecido = informacoes_favorecido['saldo_brl']

                        if cpf == cpf_favorecido:
                            messages.error(request, 'Não é permitido realizar transferência para sua mesma conta.')
                        
                        else:
    
                            #CASO POSSUA CPF EM NOSSO BANCO DE DADOS FAZEMOS A VERIFICAÇÃO SE TODOS DADOS FORAM INSERIDOS CORRETAMENTE
                           
                            #Dados para validacao da transferencia
                            verificacao_cpf_usuario = informacoes_favorecido['cpf']
                            verificacao_agencia_usuario = informacoes_favorecido['agencia']
                            verificacao_conta_usuario = informacoes_favorecido['conta']
                            verificacao_digito_usuario = informacoes_favorecido['digito_conta']

                            if cpf_favorecido == verificacao_cpf_usuario and agencia_favorecido == verificacao_agencia_usuario and conta_favorecido == verificacao_conta_usuario and digito_conta_favorecido == verificacao_digito_usuario:
                                novo_saldo = float(saldo_favorecido) + valor_transferencia
                                atualizar_saldo = Perfil.objects.update_or_create(cpf= cpf_favorecido, defaults={'saldo_brl': novo_saldo},)

                                novo_saldo_desconto = float(saldo) - valor_transferencia
                                atualizar_saldo = Perfil.objects.update_or_create(user_id= id_usuario, defaults={'saldo_brl': novo_saldo_desconto},)

                                transferencia_save(id_usuario, numero_operacao, banco_favorecido, cpf_favorecido, valor_formatado, nome_favorecido, agencia_favorecido, conta_favorecido, digito_conta_favorecido, cpf, conta, digito_conta, agencia )
                                
                                messages.success(request, 'Transferência realizada com sucesso!')

                            else:
                                messages.error(request, 'Transferência não realizada. Verifique se os dados do favorecido foram inseridos corretamente.')
                    else:
                        messages.error(request, 'Transferência não realizada, não possuímos conta com o CPF ' + cpf_favorecido + ' cadastrado em nosso sistema. Verifique se foram inseridos os dados corretamente.')

                else:
                    #SE A TRANSFERENCIA NÃO FOR PARA NOSSO BANCO AQUI DEVE SEGUIR O PROCESSO PARA BANCO EXTERNO
                    novo_saldo = float(saldo) - valor_transferencia
                    atualizar_saldo = Perfil.objects.update_or_create(user_id= id_usuario, defaults={'saldo_brl': novo_saldo},)

                    #AQUI CHAMO A FUNÇÃO TRANSFERENCIA_SAVE PARA PASSAR OS DADOS E SALVAR SE ESTIVER TUDO OKAY
                    transferencia_save(id_usuario, numero_operacao, banco_favorecido, cpf_favorecido, valor_formatado, nome_favorecido, agencia_favorecido, conta_favorecido, digito_conta_favorecido, cpf, conta, digito_conta, agencia )

                    messages.success(request, 'Transferência realizada com sucesso!')

                

        else:
            messages.error(request, 'Saldo insuficiente R$ ' + str(saldo))
            print("Saldo insuficiente R$ " + str(saldo))
            
        

        

        return redirect ('dashboard')
    else:
        return redirect ('dashboard')

def campo_vazio (campo):
    return not campo.strip()

def validacao_senhas (senha, confirmacao_senha):
    return senha != confirmacao_senha

def exibir(request):

    informacoes = Perfil.objects.all()

    dados = {
        'informacoes' : informacoes
    }


    return render(request, 'usuarios/dashboard.html', dados )

def transferencia_save(id_usuario, numero_operacao, banco_favorecido, cpf_favorecido, valor_formatado, nome_favorecido, agencia_favorecido, conta_favorecido, digito_conta_favorecido, cpf, conta, digito_conta, agencia ):
    transferencia = Transferencia.objects.create(
        nome_usuario= id_usuario, 
        numero_operacao = numero_operacao, 
        banco_favorecido = banco_favorecido, 
        cpf_favorecido = cpf_favorecido,
        valor_transferido = valor_formatado,
        nome_favorecido = nome_favorecido,
        agencia_favorecido = agencia_favorecido,
        conta_favorecido = conta_favorecido,
        digito_conta_favorecido = digito_conta_favorecido,

        operacao = 'teste',
        cpf_usuario = cpf,
        conta_usuario = conta,
        digito_conta_usuario = digito_conta,
        agencia_usuario = agencia
    )

    return transferencia.save()


    