# Desafio Extra:
# Após concluir a modelagem das classes e a criação dos métodos, atualize os
# métodos que tratam as opções do menu para funcionarem com as classes
# modeladas.

import textwrap
from abc import ABC
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] # Iniciamos sem conta (este argumento não foi passado para o construtor).
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta) # Adiciona a conta recebida por parâmetro no array de contas.

class PessoaFisica(Cliente):
    # A classe PessoaFisica se estende da classe Cliente.
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco) # Chamamos o contrutor da classe py Cliente passando o endereço.
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero): # Recebe cliente e numero.
        return cls(numero, cliente) # Retorna uma instância de conta.

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
        
    @property
    def agencia(self):
        return self._agencia
        
    @property
    def cliente(self):
        return self._cliente
        
    @property
    def numero(self):
        return self._numero
        
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo: # Valor maior que o saldo.
            print("\nA operação falhou! Você não tem saldo suficiente.")
            
        elif valor > 0: # Valor é maior que 0 sem ter entrado no if anterior.
            self._saldo -= valor # O valor informado é debitado do saldo.
            ("\nSaque realizado com sucesso!")
            return True
        
        else: # Não excedeu o saldo, mas o valor não é maior 0, significa que foi informado um valor negativo.
            print("\nA operação falhou! O valor informado é inválido.")
        
        return False # Se não entrou no elif, o retorno será falso (if ou else).
    
    def depositar(self, valor):
        if valor > 0: # Verificando se o valor é maior que 0.
            self._saldo += valor # Se for maior que 0, o valor informado será somado ao saldo.
            print("\nDepósito realizado com sucesso!")
        else: # Caso o valor seja menor que 0, a operação irá falhar.
            print("\nA operação falhou! O valor informado é inválido.")
            return False
        
        return True 

class ContaCorrente(Conta):
    # A ContaCorrente se estende da classe Conta.
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente) # Chamamos o contrutor da classe py Conta passando o numero e cliente.
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        # Validações
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nA operação falhou! O valor do saque excedeu o limite.") # Caso tenha excedido o valor do limite (mesmo tendo saldo), será mostrado esta mensagem.
        
        elif excedeu_saques:
            print("\nA operação falhou! O número máximo de saques foi excedido.") # Caso tenha excedido o valor de saques (mesmo tendo saldo), será mostrado esta mensagem.

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self): # Representação da classe ContaCorrente.
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = [] # Lista de transações.

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao): # O método recebe uma transação.
        # Ele armazena essa transação na lista como um dicionário.
        self._transacoes.append(
            {
               "tipo": transacao.__class__.__name__,                   # Armazena o nome da transação que pode ser Saque ou Depósito.
               "valor": transacao.valor,                               # Armazena o valor da transação.
               "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),   # Armazena a data e hora que foi realizada.
            }
        )

class Transacao(ABC):
    # Classe abstrata com a interface de Transacao.
    @property
    def valor(self):
        pass

    @classmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    # O Saque se estende da classe Transacao.
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self) # Se a operação der certo, o histórico é adicionado na conta.

class Deposito(Transacao):
    # O Deposito se estende da classe Transacao.
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self) # Se a operação der certo, o histórico é adicionado na conta.
        
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [u]\tNovo usuário
    [c]\tNova conta
    [l]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # FIXME: não permite que o cliente escolha a conta.
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!") # Caso o CPF não seja econtrado, irá retornar essa mensagem.
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor) # Após informar o valor do depósito, é criado uma transação

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (SOMENTE NÚMEROS): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com este CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado. Fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\nOperação inválida, por favor, selecione novamente a operação desejada.")


main()