from dataclasses import dataclass

@dataclass
class User:
    def __init__(self, name, password, email):
        self.name = name
        self.password  = password
        self.email = email

    def VerificaSenha(self):
        if(len(self.password) < 8):
            print("Senha Inválida!")
    
    def __repr__(self):
        return f"User(name={self.name}, password={self.password}, email={self.email})"

Teste = User("NomeUsuario", "1234567", "teste@teste.com")
print(Teste.name)
print(Teste.password)
print(Teste.email)
print(Teste.VerificaSenha())
Teste.__repr__()