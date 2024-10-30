from dataclasses import dataclass, field
from enum import Enum
from typing import List
import datetime

@dataclass
class Livro:
    titulo: str
    autores: List[str]
    edicao: int

class Status(Enum):
    DISPONIVEL = 1
    EMPRESTADO = 2
    PERDIDO = 3

@dataclass
class Exemplar:
    livro: Livro
    status: Status = Status.DISPONIVEL
    data_emprestado: datetime.datetime=None

    def checkout(self) -> bool:
        if self.status == Status.DISPONIVEL:
            self.data_emprestado = datetime.datetime.now()
            self.status = Status.EMPRESTADO
            return True
        return False

    def retorno_livro(self) -> bool:
        if self.status == Status.EMPRESTADO:
            self.status = Status.DISPONIVEL
            self.data_emprestado = None
            return True
        return False

@dataclass
class Membro:
    ID_membro: int
    nome: str
    livros_emprestados: List[Exemplar] = field(default_factory=list)

    def emprestar_livro(self, item: Exemplar) -> bool:
        if item.checkout():
            self.livros_emprestados.append(item)
            return True
        return False

    def devolver_livro(self, item: Exemplar) -> bool:
        if item.retorno_livro():
            self.livros_emprestados.remove(item)
            return True
        return False

@dataclass
class Biblioteca:
    itens: List[Exemplar] = field(default_factory=list)
    membros: List[Membro] = field(default_factory=list)
    
    def adicionar_item(self, item: Exemplar):
        self.itens.append(item)

    def adicionar_membro(self, membro: Membro):
        self.membros.append(membro)

def main():
    Livro1 = Livro(titulo="O Pequeno Príncipe", autores=["Antoine de Saint-Exupéry"], edicao=1)
    Livro2 = Livro(titulo="Sherlock Holmes", autores=["Arthur Conan Doyle"], edicao=4)

    Exemplar1 = Exemplar(livro=Livro1)
    Exemplar2 = Exemplar(livro=Livro2)
    Exemplar3 = Exemplar(livro=Livro1)

    biblioteca = Biblioteca()

    biblioteca.adicionar_item(Exemplar1)
    biblioteca.adicionar_item(Exemplar2)
    biblioteca.adicionar_item(Exemplar3)

    print("Usuários da Biblioteca:")
    print(biblioteca.membros)

    Membro1 = Membro(ID_membro=1, nome="José")
    Membro2 = Membro(ID_membro=2, nome="Maria")
    Membro3 = Membro(ID_membro=3, nome="João")

    biblioteca.adicionar_membro(Membro1)
    biblioteca.adicionar_membro(Membro2)
    biblioteca.adicionar_membro(Membro3)

    print("Usuários da Biblioteca:")
    print(biblioteca.membros)

    # for item in biblioteca.itens:
    #     print(item)

    # print(f"Realizando Empréstimo de '{Exemplar1.livro.titulo}': {Exemplar1.checkout()}")
    # print(f"Novo Status de '{Exemplar1.livro.titulo}': {Exemplar1.status}")

    # print(f"Realizando Empréstimo de '{Exemplar1.livro.titulo}' novamente: {Exemplar1.checkout()}")

    # print(f"Realizando Devolução de '{Exemplar1.livro.titulo}': {Exemplar1.retorno_livro()}")
    # print(f"Novo Status de '{Exemplar1.livro.titulo}': {Exemplar1.status}")

    # print(f"Realizando Devolução de '{Exemplar1.livro.titulo}' novamente: {Exemplar1.retorno_livro()}")

    print(f"Empréstimo de '{Exemplar1.livro.titulo}' para '{Membro1.nome}': {Membro1.emprestar_livro(Exemplar1)}")
    print(f"Empréstimo de '{Exemplar2.livro.titulo}' para '{Membro3.nome}': {Membro1.emprestar_livro(Exemplar2)}")

if __name__ == "__main__":
    main()