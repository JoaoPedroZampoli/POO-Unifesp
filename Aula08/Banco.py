from dataclasses import dataclass, field
from typing import List

@dataclass
class Endereco:
    rua: str
    numero: int
    bairro: str
    cidade: str
    estado: str
    cep: str

@dataclass
class Cliente:
    nome: str
    cpf: str
    endereco: list[Endereco] = field(default_factory=list)
    

@dataclass
class ContaCorrente:
    titular: Cliente
    numero: str
    saldo: float = 0.0

    def credita(self, valor: float) -> None:
        self.saldo += valor

    def debita(self, valor: float) -> None:
        self.saldo -= valor

    