from typing import List, Optional
from datetime import datetime
import re

# Gerador de IDs
def id_unico():
    id = 1
    while True:
        yield id
        id += 1

gerador_ids = id_unico()

def validar_email(email: str) -> bool:
    regex_email = r"^\S+@\S+\.\S+$"
    return re.match(regex_email, email) is not None

def validar_data(data: str) -> bool:
    try:
        datetime.strptime(data, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def comparar_datas(data_inicio: str, data_fim: str) -> bool:
    return datetime.strptime(data_inicio, "%Y-%m-%d") < datetime.strptime(data_fim, "%Y-%m-%d")

def validar_nome(nome: str) -> bool:
    return bool(nome.strip())

# Classe Pessoa
class Pessoa:
    def __init__(self, nome: str, email: str):
        self._nome = nome
        self._email = email

    def mostrar_detalhes(self):
        return f"Nome: {self._nome}, Email: {self._email}"

# Classe Cliente herda de Pessoa
class Cliente(Pessoa):
    def mostrar_detalhes(self):
        return super().mostrar_detalhes()

# Classe Funcionario herda de Pessoa
class Funcionario(Pessoa):
    def __init__(self, nome, email, cargo, salario):
        super().__init__(nome, email)
        self._cargo = cargo
        self._salario = salario

    def mostrar_detalhes(self):
        return super().mostrar_detalhes() + f", Cargo: {self._cargo}, Salario: {self._salario}"

# Classe Quarto
class Quarto:
    def __init__(self, numero: int, tipo: str):
        self._numero = numero
        self._tipo = tipo

    def get_numero(self):
        return self._numero

    def get_tipo(self):
        return self._tipo

# Classe Reserva
class Reserva:
    def __init__(self, cliente: Cliente, quarto: Quarto, data_inicio: str, data_fim: str):
        self._id = next(gerador_ids)
        self._cliente = cliente
        self._quarto = quarto
        self._data_inicio = data_inicio
        self._data_fim = data_fim

# Classe Hotel
class Hotel:
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._quartos: List[Quarto] = []
        self._reservas: List[Reserva] = []

    def adicionar_cliente(self, cliente: Cliente):
        self._clientes.append(cliente)

    def adicionar_quarto(self, quarto: Quarto):
        self._quartos.append(quarto)

    def quarto_disponivel(self, quarto: Quarto, data_inicio: str, data_fim: str) -> bool:
        for reserva in self._reservas:
            if reserva._quarto == quarto:
                if not (data_fim < reserva._data_inicio or data_inicio > reserva._data_fim):
                    return False
        return True

    def fazer_reserva(self, cliente: Cliente, data_inicio: str, data_fim: str) -> Optional[str]:
        for quarto in self._quartos:
            if self.quarto_disponivel(quarto, data_inicio, data_fim):
                reserva = Reserva(cliente, quarto, data_inicio, data_fim)
                self._reservas.append(reserva)
                return f"Reserva feita com sucesso no quarto número {quarto.get_numero()}."
        return "Nenhum quarto disponível para o período selecionado"

    def listar_reservas(self):
        print("Reservas:")
        for reserva in self._reservas:
            print(f"Nome: {reserva._cliente._nome}, Tipo de quarto: {reserva._quarto.get_tipo()}, Número do quarto: {reserva._quarto.get_numero()}, Data de Início: {reserva._data_inicio}, Data de Fim: {reserva._data_fim}")

# Programa principal
hotel = Hotel()

# Adicionar alguns quartos de exemplo
hotel.adicionar_quarto(Quarto(101, "single"))
hotel.adicionar_quarto(Quarto(102, "duplo"))

while True:
    nome = input("Insira o nome do cliente: ")
    if not validar_nome(nome):
        print("Nome inválido. Tente novamente.")
        continue

    email = input("Insira o email do cliente: ")
    if not validar_email(email):
        print("Email inválido. Tente novamente.")
        continue

    cliente = Cliente(nome, email)
    hotel.adicionar_cliente(cliente)

    data_inicio = input("Insira a data de início da reserva (AAAA-MM-DD): ")
    data_fim = input("Insira a data de fim da reserva (AAAA-MM-DD): ")
    if not (validar_data(data_inicio) and validar_data(data_fim) and comparar_datas(data_inicio, data_fim)):
        print("Datas inválidas. Tente novamente.")
        continue

    resultado = hotel.fazer_reserva(cliente, data_inicio, data_fim)

    if resultado:
        print(resultado)

    continuar = input("Deseja fazer outra reserva? (s/n): ")
    if continuar.lower() != 's':
        break

hotel.listar_reservas()
