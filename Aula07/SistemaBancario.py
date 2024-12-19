from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

# @dataclass
# class Endereco:
#     rua: str
#     numero: int
#     bairro: str
#     cidade: str
#     estado: str
#     cep: str

@dataclass
class Transacao:
    data: datetime
    tipo: str
    valor: float

@dataclass
class ContaBancaria(ABC):
    titular: str
    saldo: float
    numero: str
    historico: List[Transacao] = field(default_factory=list)

    @abstractmethod
    def sacar(self):
        pass

    def depositar(self, valor: float):
        self.saldo += valor
        self.historico.append(Transacao(datetime.now(), "Depósito", valor))
    
    def consultar_saldo(self):
        return print(f"Conta: {self.numero} Saldo: {self.saldo}")

    def extrato(self):
        print(f"Extrato da conta {self.numero} de {self.titular}:")
        for transacao in self.historico:
            print(f"Data: {transacao.data.day}/{transacao.data.month}/{transacao.data.year} {transacao.data.hour}:{transacao.data.minute}:{transacao.data.second} Tipo: {transacao.tipo} Valor: {transacao.valor}")
        print(f"Saldo atual: {self.saldo}")
        if(self.__class__.__name__ == "ContaCorrente"):
            print(f"Cheque Especial Disponível: {self.limiteChequeEspecial-(-self.saldo)}")

    def transferencia(self, valor: float, contaDestino):
        if self.saldo >= valor:
            self.saldo -= valor
            contaDestino.depositar(valor)
            self.historico.append(Transacao(datetime.now(), "Transferência (envio)", valor))
            contaDestino.historico.append(Transacao(datetime.now(), "Transferência (recebimento)", valor))
            return True
        return False

@dataclass
class ContaCorrente(ContaBancaria):
    limiteChequeEspecial: float = 0.0

    # def depositar(self, valor: float):
    #     self.saldo += valor

    def definir_limite_cheque_especial(self, valor: float):
        self.limiteChequeEspecial = valor

    def sacar(self, valor: float):
        saldoDisponivel = self.saldo + self.limiteChequeEspecial
        if saldoDisponivel >= valor:
            self.saldo -= valor
            if self.saldo < 0:
                self.historico.append(Transacao(datetime.now(), "Saque (com uso de cheque especial)", valor))
            else:
                self.historico.append(Transacao(datetime.now(), "Saque", valor))
            return True
        else:
            print("Saldo insuficiente")
            return False

@dataclass
class ContaPoupanca(ContaBancaria):
    jurosRendimento: float = 0.05 
    qtdSaquesDiarios: int = 0
    LimiteSaquesDiarios: int = 3

    # def depositar(self, valor: float):
    #     self.saldo += valor

    def sacar(self, valor: float):
        if self.qtdSaquesDiarios < self.LimiteSaquesDiarios:
            if self.saldo >= valor:
                self.saldo -= valor
                self.historico.append(Transacao(datetime.now(), "Saque", valor))
                self.qtdSaquesDiarios += 1
                return True
            else:
                print("Saldo insuficiente")
                return False
        else:
            print("Limite de saques diários atingido")
            return False

    def render_juros(self):
        ultimoJuros = self.historico[-1].data
        if datetime.now().month != ultimoJuros.month: #Para visualizar o rendimento, é necessário comentar essa verificação, caso contrário, só haverá um rendimento em um intervalo de um mês
            self.saldo += self.saldo * self.jurosRendimento
            self.historico.append(Transacao(datetime.now(), f"Rendimento do mês {datetime.now().month}/{datetime.now().year}", self.saldo * self.jurosRendimento))

@dataclass
class Cliente:
    nome: str
    cpf: str
    enderecos: List[str]
    contas: List[ContaBancaria]

    def adicionar_conta(self, conta: ContaBancaria):
        self.contas.append(conta)

    def remover_conta(self, numero_conta: str):
        for conta in self.contas:
            if conta.numero == numero_conta:
                self.contas.remove(conta)
                return
        print("Conta não encontrada")

    def listagem_contas(self):
        for conta in self.contas:
            if conta.__class__.__name__ == "ContaCorrente":
                print(f"Conta Corrente: {conta.numero} Saldo: {conta.saldo} Limite Cheque Especial: {conta.limiteChequeEspecial}")
            else:
                print(f"Conta Poupança: {conta.numero} Saldo: {conta.saldo}")

    def adicionar_endereco(self, endereco: str):
        self.enderecos.append(endereco)

    def remover_endereco(self, endereco: str):
        if endereco in self.enderecos:
            self.enderecos.remove(endereco)

def main():
    # Endereco1 = Endereco("Rua 1", 123, "Bairro 1", "Cidade 1", "Estado 1", "12345-678")
    cliente1 = Cliente("João", "123.456.789-00", ["Avenida Vital Brasil, 1177", "Rua Uberto Marino"], [])
    conta1 = ContaCorrente("João", 1000, "1234", [Transacao(datetime.now(), "Depósito", 1000)])
    conta2 = ContaPoupanca("João", 1000, "1235", [Transacao(datetime.now(), "Depósito", 1000)])
    cliente1.adicionar_conta(conta1)
    conta1.definir_limite_cheque_especial(100)
    cliente1.adicionar_conta(conta2)

    cliente2 = Cliente("Maria", "987.654.321-00", ["Rua Barão de Cocaes, 340"], [])
    conta3 = ContaCorrente("Maria", 2000, "1236", [Transacao(datetime.now(), "Depósito", 2000)])
    cliente2.adicionar_conta(conta3)

    cliente1.listagem_contas()
    cliente2.listagem_contas()

    conta1.depositar(500)
    conta1.consultar_saldo()

    conta1.sacar(200)
    conta1.consultar_saldo()

    conta1.sacar(2000)
    conta1.consultar_saldo()

    conta1.transferencia(500, conta2)
    conta1.transferencia(100, conta3)
    conta1.consultar_saldo()
    conta2.consultar_saldo()
    conta3.consultar_saldo()

    conta1.sacar(800)
    conta1.consultar_saldo()

    conta2.consultar_saldo()
    conta2.render_juros()
    conta2.consultar_saldo()

    conta1.extrato()
    conta2.extrato()

    conta2.sacar(100)
    conta2.consultar_saldo()
    conta2.sacar(100)
    conta2.consultar_saldo()
    conta2.sacar(100)
    conta2.consultar_saldo()
    conta2.sacar(100)

if __name__ == "__main__":
    main()