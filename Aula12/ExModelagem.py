from dataclasses import dataclass
import time


@dataclass
class Coordenada:
    x: float
    y: float


@dataclass
class Servico:
    TipoServico: str
    ValorBase: float
    TarifaKm: float
    TarifaMinuto: float


def CalculoDeDistancia(CoordenadaInicial: Coordenada, CoordenadaFinal: Coordenada):
    return ((CoordenadaInicial.x - CoordenadaFinal.x) ** 2 + (CoordenadaInicial.y - CoordenadaFinal.y) ** 2) ** 0.5


def CalculoDeTempo(Distancia: float, VelocidadeMedia: float = 40.0):
    return (Distancia / VelocidadeMedia) * 60


@dataclass
class Viagem:
    TarifaBase: float
    Distancia: float
    TarifaKm: float
    TarifaMinuto: float
    Tempo: float
    Gorjeta: float = 0.0
    MultiplicadorDemanda: float = 1.0
    TaxaServico: float = 0.25

    def CalculoTarifaBruta(self):
        TarifaDistancia = self.Distancia * self.TarifaKm
        TarifaTempo = self.Tempo * self.TarifaMinuto
        return ((self.TarifaBase + TarifaDistancia + TarifaTempo) * self.MultiplicadorDemanda)/3 + self.Gorjeta

    def CalculoTarifaMotorista(self):
        return self.CalculoTarifaBruta() * (1 - self.TaxaServico)


@dataclass
class Motorista:
    Nome: str
    CategoriaServico: str
    Saldo: float

    def AtualizarSaldo(self, valor: float):
        self.Saldo += valor


@dataclass
class Cliente:
    Nome: str
    Saldo: float
    Localizacao: Coordenada

    def PagarViagem(self, valor: float):
        if valor > self.Saldo:
            raise ValueError("Saldo insuficiente")
        self.Saldo -= valor

def processar_pagamento(cliente, motorista, viagem):
    tarifa_cliente = viagem.CalculoTarifaBruta()
    tarifa_motorista = viagem.CalculoTarifaMotorista()
    try:
        cliente.PagarViagem(tarifa_cliente)
        motorista.AtualizarSaldo(tarifa_motorista)
        print(f"Viagem concluída com sucesso para {cliente.Nome}!")
        print(f"Tarifa cobrada do cliente: R${tarifa_cliente:.2f}")
        print(f"Tarifa paga ao motorista: R${tarifa_motorista:.2f}")
        print(f"Saldo do cliente {cliente.Nome}: R${cliente.Saldo:.2f}")
        print(f"Saldo do motorista {motorista.Nome}: R${motorista.Saldo:.2f}\n")
    except ValueError as e:
        print(f"Erro ao processar pagamento de R$ {tarifa_cliente:.2f} em nome de {cliente.Nome}: {e}\n")

def main():
    cliente1 = Cliente("João", 150.0, Coordenada(10, 10))
    cliente2 = Cliente("Maria", 100.0, Coordenada(20, 30))
    cliente3 = Cliente("Luisa", 200.0, Coordenada(40, 50))

    motorista1 = Motorista("Carlos", "UberX", 50.0)
    motorista2 = Motorista("Ana", "UberEco", 100.0)
    motorista3 = Motorista("Pedro", "UberBlack", 150.0)

    servico1 = Servico("UberX", ValorBase=5.0, TarifaKm=2.0, TarifaMinuto=0.5)
    servico2 = Servico("UberEco", ValorBase=10.0, TarifaKm=3.0, TarifaMinuto=1.0)
    servico3 = Servico("UberBlack", ValorBase=15.0, TarifaKm=4.0, TarifaMinuto=1.5)

    inicio = Coordenada(10, 10)
    destino = Coordenada(20, 30)

    distancia = CalculoDeDistancia(inicio, destino)
    tempo = CalculoDeTempo(distancia)

    viagem1 = Viagem(
        TarifaBase=servico1.ValorBase,
        Distancia=distancia,
        TarifaKm=servico1.TarifaKm,
        TarifaMinuto=servico1.TarifaMinuto,
        Tempo=tempo,
        Gorjeta=10.0,
        MultiplicadorDemanda=1.5
    )
    
    viagem2 = Viagem(
        TarifaBase=servico2.ValorBase,
        Distancia=distancia,
        TarifaKm=servico2.TarifaKm,
        TarifaMinuto=servico2.TarifaMinuto,
        Tempo=tempo,
        Gorjeta=5.0,
        MultiplicadorDemanda=1.2
    )
    
    viagem3 = Viagem(
        TarifaBase=servico3.ValorBase,
        Distancia=distancia,
        TarifaKm=servico3.TarifaKm,
        TarifaMinuto=servico3.TarifaMinuto,
        Tempo=tempo,
        Gorjeta=15.0,
        MultiplicadorDemanda=1.3
    )

    processar_pagamento(cliente1, motorista1, viagem1)
    processar_pagamento(cliente2, motorista2, viagem2)
    processar_pagamento(cliente3, motorista3, viagem3)

if __name__ == "__main__":
    main()
