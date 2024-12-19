from abc import ABC, abstractmethod
from dataclasses import dataclass

class Pet(ABC):

    @abstractmethod
    def Fazer_Som(self):
        pass

class Cachorro(Pet):

    def Fazer_Som(self):
        print("Cachorro faz som de latido")
        print("Au Au")
    
class Gato(Pet):

    def Fazer_Som(self):
        print("Gato faz som de miado")
        print("Miau")

@dataclass
class Pessoa:
    pet: Pet

    def Interagir(self):
        self.pet.Fazer_Som()

def main():
    toto = Cachorro()
    Maria = Pessoa(toto)

    Maria.Interagir()

main()

