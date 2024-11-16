

import os
import json
import re
import oracledb

# Conexão ao Banco de Dados

def conectar_db():
    try:
        # Conectar ao banco de dados Oracle
        conn = oracledb.connect(
            user="", 
            password="", 
            dsn=""
        )
        return conn
    except oracledb.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas():
    # Defina o comando SQL para criar as tabelas
    create_usuarios_table = """
    CREATE TABLE T_USER (
        id NUMBER PRIMARY KEY,
        email VARCHAR2(255) UNIQUE,
        senha VARCHAR2(255),
        cpf VARCHAR2(11)
    );
    """

    create_pontos_table = """
    CREATE TABLE T_PONTOS (
        id NUMBER PRIMARY KEY,
        usuario_id NUMBER,
        pontos NUMBER,
        FOREIGN KEY (usuario_id) REFERENCES T_user(id)
    );
    """

    # Conectar ao banco de dados
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Criar as tabelas no banco de dados
            cursor.execute(create_usuarios_table)
            cursor.execute(create_pontos_table)
            conn.commit()
            print("Tabelas 'T_USER' e 'T_PONTOS' criadas com sucesso.")
        except oracledb.Error as e:
            print(f"Erro ao criar as tabelas: {e}")
        finally:
            cursor.close()
            conn.close()

# Chama a função para criar as tabelas
criar_tabelas()

# Adiciona uma pausa para ver as mensagens
input("Pressione Enter para sair...")


# MENSAGENS 
MSG_CADASTRO_SUCESSO = "Cadastro realizado com sucesso!"
MSG_CADASTRO_USUARIO = "Usuário cadastrado com sucesso!"
MSG_OPCAO_INVALIDA = "Opção inválida. Por favor, escolha novamente."
MSG_NENHUM_CADASTRO = "Nenhum cadastro encontrado."
MSG_PROBLEMA_RELATADO = "Avaliação relatada com sucesso!"
MSG_PROBLEMA_REMOVIDO = "Avaliação removida com sucesso!"
MSG_EMAIL_INVALIDO = "E-mail inválido! Não é possível realizar esta ação."
MSG_SENHA_INVALIDA = "A senha precisa ter pelo menos 8 caracteres."
MSG_PONTOS_INSUFICIENTES = "Você não tem pontos suficientes para resgatar."

# ARMAZENAMENTO
cadastro_pessoal = []
problemas = {}
pontos = {}

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# VALIDAÇÃO
def validar_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validar_senha(senha):
    return len(senha) >= 8

#  CADASTRO PESSOAL
def validar_cpf(cpf):
    # Validação simples de CPF: 11 dígitos numéricos
    return cpf.isdigit() and len(cpf) == 11

def adicionar_pessoal(email, senha, cpf):
    if not validar_email(email):
        print(MSG_EMAIL_INVALIDO)
        input("\nPressione Enter para voltar ao menu...")
        return
    if not validar_senha(senha):
        print(MSG_SENHA_INVALIDA)
        input("\nPressione Enter para voltar ao menu...")
        return
    if not validar_cpf(cpf):
        print("CPF inválido! Certifique-se de que contém 11 dígitos numéricos.")
        input("\nPressione Enter para voltar ao menu...")
        return
    if buscar_pessoal_por_email(email):
        print("Este e-mail já está cadastrado.")
        input("\nPressione Enter para voltar ao menu...")
        return
    # Adicionando o CPF ao cadastro
    cadastro_pessoal.append({"email": email, "senha": senha, "cpf": cpf})
    print(MSG_CADASTRO_USUARIO)
    input("\nPressione Enter para voltar ao menu...")
def listar_pessoal():
    limpar_tela()
    if not cadastro_pessoal:
        print(MSG_NENHUM_CADASTRO)
    else:
        for i, pessoal in enumerate(cadastro_pessoal, 1):
            print(f"{i}. E-mail: {pessoal['email']}")
    input("\nPressione Enter para voltar ao menu...")
def buscar_pessoal_por_email(email):
    for pessoal in cadastro_pessoal:
        if pessoal["email"] == email:
            return pessoal
    return None
def alterar_pessoal(email_antigo, email_novo, senha_nova):
    pessoal = buscar_pessoal_por_email(email_antigo)
    if pessoal:
        pessoal["email"] = email_novo
        pessoal["senha"] = senha_nova
        print("Cadastro alterado com sucesso.")
    else:
        print("Cadastro não encontrado.")
    input("\nPressione Enter para voltar ao menu...")
def remover_pessoal(email, senha):
    global cadastro_pessoal
    pessoal_a_remover = [pessoal for pessoal in cadastro_pessoal if pessoal["email"] == email and pessoal["senha"] == senha]
    if pessoal_a_remover:
        cadastro_pessoal = [pessoal for pessoal in cadastro_pessoal if not (pessoal["email"] == email and pessoal["senha"] == senha)]
        print("Cadastro removido com sucesso.")
    else:
        print("E-mail ou senha incorretos, ou cadastro não encontrado.")
    input("\nPressione Enter para voltar ao menu...")


# GERENCIAMENTO DE PONTOS
def atribuir_pontos(email, pontos_a_adicionar):
    if email in pontos:
        pontos[email] += pontos_a_adicionar
    else:
        pontos[email] = pontos_a_adicionar
    print(f"Pontos atribuídos com sucesso! {email} agora tem {pontos[email]} pontos.")
    input("\nPressione Enter para voltar ao menu...")
def visualizar_pontos(email):
    if email in pontos:
        print(f"{email} tem {pontos[email]} pontos.")
    else:
        print(f"{email} não tem pontos registrados.")
    input("\nPressione Enter para voltar ao menu...")
def resgatar_pontos(email, pontos_resgatar):
    if email in pontos and pontos[email] >= pontos_resgatar:
        pontos[email] -= pontos_resgatar
        print(f"{pontos_resgatar} pontos resgatados com sucesso!")
    else:
        print(MSG_PONTOS_INSUFICIENTES)
    input("\nPressione Enter para voltar ao menu...")


# RELATAR PROBLEMAS
def relatar_problema(descricao_problema, email):
    if not validar_email(email):
        print("E-mail inválido! Não é possível relatar o avaliação.")
        input("\nPressione Enter para voltar ao menu...")
        return  
    problema_id = len(problemas) + 1
    problemas[problema_id] = descricao_problema
    print(MSG_PROBLEMA_RELATADO)
    input("\nPressione Enter para voltar ao menu...")
def listar_problemas():
    limpar_tela()
    if not problemas:
        print("Nenhuma avaliação relatada.")
    else:
        for problema_id, descricao in problemas.items():
            print(f"ID: {problema_id} - Descrição: {descricao}")
    input("\nPressione Enter para voltar ao menu...")
def remover_problema(problema_id):
    if problema_id in problemas:
        del problemas[problema_id]
        print(MSG_PROBLEMA_REMOVIDO)
    else:
        print("Avaliação não encontrada.")
    input("\nPressione Enter para voltar ao menu...")


# JSON
def exportar_dados_json():
    dados = {
        "cadastro_pessoal": cadastro_pessoal,
        "problemas": problemas,
        "pontos": pontos
    }
    with open("dados.json", "w") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4)
    print("Dados exportados para dados.json com sucesso!")
    input("\nPressione Enter para voltar ao menu...")

# FUNÇÕES DE ENTRADA
def adicionar_cadastro_entrada():
    limpar_tela()
    print("Cadastro de novo usuário")
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")
    cpf = input("Digite o CPF (somente números): ")
    adicionar_pessoal(email, senha, cpf)
def alterar_cadastro_entrada():
    limpar_tela()
    print("=== Alterar Cadastro Pessoal ===")
    email_antigo = input("Digite o e-mail antigo: ")
    email_novo = input("Digite o novo e-mail: ")
    senha_nova = input("Digite a nova senha: ")
    alterar_pessoal(email_antigo, email_novo, senha_nova)
def remover_cadastro_entrada():
    limpar_tela()
    print("=== Remover Cadastro Pessoal ===")
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")
    remover_pessoal(email, senha)

# Cadastro de Pontos
acoes_disponiveis = {
    "plantou uma arvore": 10,
    "coletou lixo": 5,
    "reduziu consumo de plástico": 8,
    "participou de um evento sustentável": 12,
}
def atribuir_pontos_entrada():
    limpar_tela()
    print("=== Atribuir Pontos ===")
    email = input("Digite o e-mail do usuário: ")
    if not buscar_pessoal_por_email(email):
        print("Usuário não encontrado.")
        input("\nPressione Enter para voltar ao menu...")
        return
    print("\nEscolha uma das ações abaixo:")
    for i, (acao, pontos) in enumerate(acoes_disponiveis.items(), 1):
        print(f"{i}. {acao.capitalize()} - {pontos} pontos")
    while True:
        try:
            escolha = int(input("\nDigite o número da ação realizada pelo usuário: "))
            if 1 <= escolha <= len(acoes_disponiveis):
                acao_selecionada = list(acoes_disponiveis.keys())[escolha - 1]
                pontos_a_adicionar = acoes_disponiveis[acao_selecionada]
                break
            else:
                print("Erro: Escolha inválida. Digite um número da lista.")
        except ValueError:
            print("Erro: Entrada inválida. Digite um número válido.")
    
    # Chama a função para atribuir os pontos ao usuário
    atribuir_pontos(email, pontos_a_adicionar, acao_selecionada)

def atribuir_pontos(email, pontos_a_adicionar, acao_selecionada):
    usuario = buscar_pessoal_por_email(email)
    if usuario:
        if "pontos" not in usuario:
            usuario["pontos"] = 0
        usuario["pontos"] += pontos_a_adicionar  # Soma os pontos
        if "acoes" not in usuario:
            usuario["acoes"] = []
        usuario["acoes"].append({"acao": acao_selecionada, "pontos": pontos_a_adicionar})  # Adiciona a ação
        pontos[email] = usuario["pontos"]  # Garante que os pontos sejam armazenados no dicionário
        print(f"Pontos atribuídos com sucesso! {pontos_a_adicionar} pontos para a ação: {acao_selecionada.capitalize()}")
    else:
        print("Usuário não encontrado.")
    input("\nPressione Enter para voltar ao menu...")

def listar_acoes_usuario(email):
    usuario = buscar_pessoal_por_email(email)
    if usuario and "acoes" in usuario:
        print(f"Ações de {email}:")
        for i, acao in enumerate(usuario["acoes"], 1):
            print(f"{i}. Ação: {acao['acao'].capitalize()} - Pontos: {acao['pontos']}")
    else:
        print("Nenhuma ação registrada ou usuário não encontrado.")
    input("\nPressione Enter para voltar ao menu...")

def visualizar_pontos(email):
    if email in pontos:
        print(f"{email} tem {pontos[email]} pontos.")
    else:
        print(f"{email} não tem pontos registrados.")
    input("\nPressione Enter para voltar ao menu...")

def visualizar_pontos_entrada():
    limpar_tela()
    print("=== Visualizar Pontos ===")
    email = input("Digite o e-mail do usuário: ")
    visualizar_pontos(email)
def resgatar_pontos_entrada():
    limpar_tela()
    print("=== Resgatar Pontos ===")
    email = input("Digite o e-mail do usuário: ")
    
    while True:
        try:
            pontos_resgatar = int(input("Digite a quantidade de pontos a ser resgatada: "))
            if pontos_resgatar <= 0:
                print("Por favor, insira um valor positivo.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

    # Aqui você chama a função de resgate, por exemplo:
    resgatar_pontos(email, pontos_resgatar)
def relatar_problema_entrada():
    limpar_tela()
    print("=== Avaliar Sistema ===")
    descricao_problema = input("Digite a descrição da Avaliação: ")
    email = input("Digite seu e-mail: ")
    relatar_problema(descricao_problema, email)

def remover_problema_entrada():
    limpar_tela()
    print("=== Remover Avaliação ===")
    
    while True:
        try:
            problema_id = int(input("Digite o número da avaliação a ser removida: "))
            if problema_id > 0:
                break
            else:
                print("Por favor, insira um número maior que zero.")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    remover_problema(problema_id)
# MENU PRINCIPAL
def menu_principal():
    while True:
        limpar_tela()
        print("=== MENU PRINCIPAL ===")
        print("1. Gerenciar Cadastro Pessoal")
        print("2. Gerenciar Pontos")
        print("3. Avaliar Sistema")
        print("4. Exportar dados para JSON")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            menu_cadastros()
        elif opcao == "2":
            menu_pontos()
        elif opcao == "3":
            menu_problemas()
        elif opcao == "4":
            exportar_dados_json()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print(MSG_OPCAO_INVALIDA)
            input("\nPressione Enter....")

# MENU DE CADASTRO
def menu_cadastros():
    while True:
        limpar_tela()
        print("1. Adicionar Cadastro Pessoal")
        print("2. Listar Cadastros")
        print("3. Alterar Cadastro")
        print("4. Remover Cadastro")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            adicionar_cadastro_entrada()
        elif opcao == "2":
            listar_pessoal()
        elif opcao == "3":
            alterar_cadastro_entrada()
        elif opcao == "4":
            remover_cadastro_entrada()
        elif opcao == "0":
            break
        else:
            print(MSG_OPCAO_INVALIDA)
            input("\nPressione o Enter...")

# MENU DE PONTOS
def menu_pontos():
    while True:
        limpar_tela()
        print("1. Atribuir Pontos")
        print("2. Visualizar Pontos")
        print("3. Resgatar Pontos")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            atribuir_pontos_entrada()
        elif opcao == "2":
            visualizar_pontos_entrada()
        elif opcao == "3":
            resgatar_pontos_entrada()
        elif opcao == "0":
            break
        else:
            print(MSG_OPCAO_INVALIDA)
            input("\nPressione Enter...")

# MENU DE PROBLEMAS
def menu_problemas():
    while True:
        limpar_tela()
        print("1. Nova Avaliação ")
        print("2. Listar Avaliações ")
        print("3. Remover Avaliação")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            relatar_problema_entrada()
        elif opcao == "2":
            listar_problemas()
        elif opcao == "3":
            remover_problema_entrada()
        elif opcao == "0":
            break
        else:
            print(MSG_OPCAO_INVALIDA)
            input("\nPressione o Enter...")

# EXECUÇÃO DO MENU PRINCIPAL
menu_principal()
