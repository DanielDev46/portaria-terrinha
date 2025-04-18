import json
import os

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_PLACAS = "placas.json"

# Dicionários para armazenar dados
usuarios = {}
placas = {}
usuarios_placas = {}

# Função para carregar dados do arquivo JSON
def carregar_dados():
    global usuarios, placas, usuarios_placas
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            dados = json.load(f)
            usuarios = dados.get("usuarios", {})
            usuarios_placas = dados.get("usuarios_placas", {})
    else:
        usuarios = {"Daniel": 1234, "Gustavo.barbosa": 5933}
        usuarios_placas = {"Daniel": [], "Gustavo.barbosa": []}

    if os.path.exists(ARQUIVO_PLACAS):
        with open(ARQUIVO_PLACAS, "r") as f:
            placas = json.load(f)
    else:
        placas.update({
            22: "Motorista: GENILSON - Veículo: Carreta - Placa: HEX2203",
            20: "Motorista: DANIEL - Veículo: Truck - Placa: TXT2003"
        })

# Função para salvar os usuários e placas em arquivos JSON
def salvar_dados():
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump({"usuarios": usuarios, "usuarios_placas": usuarios_placas}, f, indent=4)
    with open(ARQUIVO_PLACAS, "w") as f:
        json.dump(placas, f, indent=4)

# Função de login
def realizar_login():
    usuario = input("Digite seu usuário: ")
    senha = int(input("Digite sua senha: "))

    if usuarios.get(usuario) == senha:
        print("Usuário e senha validados com sucesso!")
        menu_login(usuario)
    else:
        print("Usuário ou senha inválidos!")

# Menu após login
def menu_login(usuario):
    while True:
        print("\n1 - Consultar placas cadastradas")
        print("2 - Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            consultar_placas()
        elif opcao == "2":
            break
        else:
            print("Opção inválida!")

# Função para consultar placas
def consultar_placas():
    placa_consultada = int(input("Digite os dois primeiros números da placa: "))
    if placa_consultada in placas:
        print("Placa encontrada:", placas[placa_consultada])
    else:
        print("Placa não encontrada!")

# Função para cadastrar um novo usuário
def cadastrar_usuario():
    nome = input("Digite o nome do novo usuário: ")
    if nome in usuarios:
        print("Usuário já existe!")
        return

    senha = int(input("Digite a senha: "))
    usuarios[nome] = senha
    usuarios_placas[nome] = []
    salvar_dados()
    print("Usuário cadastrado com sucesso!")

# Função para cadastrar uma nova placa
def cadastrar_placa():
    placa = int(input("Digite os dois primeiros números da placa: "))
    if placa in placas:
        print("Placa já cadastrada!")
        return

    motorista = input("Digite o nome do motorista: ")
    tipo_veiculo = input("Digite o tipo de veículo: ")
    placas[placa] = f"Motorista: {motorista} - Veículo: {tipo_veiculo} - Placa: {placa}"
    
    usuario = input("Digite seu usuário para vincular a placa: ")
    if usuario in usuarios:
        usuarios_placas[usuario].append(placa)
        salvar_dados()
        print("Placa cadastrada com sucesso!")
    else:
        print("Usuário não encontrado!")

# Menu principal
def menu_principal():
    carregar_dados()

    while True:
        print("\n1 - Login")
        print("2 - Cadastrar novo usuário")
        print("3 - Cadastrar nova placa")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            realizar_login()
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            cadastrar_placa()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

# Iniciar o programa
if __name__ == "__main__":
    menu_principal()
