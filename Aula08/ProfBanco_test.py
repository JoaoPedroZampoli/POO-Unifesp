from Banco import Endereco, Cliente, ContaCorrente

def test_credita_100():
    endereco = Endereco(rua = "Avenida Vital Brasil", numero=1177, bairro="Butantã", cidade="São Paulo", estado="SP", cep="05503-001")
    cliente = Cliente(nome="João", cpf="123.456.789-00", enderecos=[endereco])
    conta = ContaCorrente(titular=cliente, numero="90993-1")
    conta.credita(100.0)
    assert conta.saldo == 100.0
                    
def test_debita_100():
    endereco = Endereco(rua = "Avenida Vital Brasil", numero=1177, bairro="Butantã", cidade="São Paulo", estado="SP", cep="05503-001")
    cliente = Cliente(nome="João", cpf="123.456.789-00", enderecos=[endereco])
    conta = ContaCorrente(titular=cliente, numero="90993-1")
    conta.credita(100.0)
    conta.debita(100.0)
    assert conta.saldo == 0.0