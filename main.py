# -- RM: 554635 - Lucas Lerri de Almeida - Turma: 1TDSPI - Professor: Edson de Oliveira
# -- RM: 557591 - João Pedro C. Zanni - Turma: 1TDSPI - Professor: Edson de Oliveira
# -- RM: 556459 - Rafael Bompadre Lima - Turma: 1TDSPH - Professor: Fernando Luiz de Almeida


import os
import json
import re
import oracledb


# Conexão com o BD 
def conectar_db():
    try:
        conn = oracledb.connect(
            user="rm557591", 
            password="fiap24", 
            dsn="oracle.fiap.com.br:1521/ORCL"
        )
        return conn
    except oracledb.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    

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
    # Valida formato padrão de email
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))

def validar_senha(senha):
    # Mínimo 8 caracteres, pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial
    padrao = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(padrao, senha))

def validar_cpf(cpf):
    # Verifica se o CPF tem 11 dígitos numéricos
    return cpf.isdigit() and len(cpf) == 11

# Validações
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


# Conexão com o CRUD do Gerenciamento de Cadastro Pessoal
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            insert_query = """
            INSERT INTO T_USER (email, senha, cpf) 
            VALUES (:email, :senha, :cpf)
            """
            cursor.execute(insert_query, {'email': email, 'senha': senha, 'cpf': cpf})
            conn.commit()  
            print(MSG_CADASTRO_USUARIO)
        except oracledb.Error as e:
            print(f"Erro ao adicionar o usuário ao banco de dados: {e}")
        finally:
            cursor.close()
            conn.close()
    input("\nPressione Enter para voltar ao menu...")

def listar_pessoal():
    limpar_tela()
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT email FROM T_USER")
            usuarios = cursor.fetchall()
            if not usuarios:
                print(MSG_NENHUM_CADASTRO)
            else:
                for i, usuario in enumerate(usuarios, 1):
                    print(f"{i}. E-mail: {usuario[0]}")
        except oracledb.Error as e:
            print(f"Erro ao listar os usuários: {e}")
        finally:
            cursor.close()
            conn.close()
    input("\nPressione Enter para voltar ao menu...")

def buscar_pessoal_por_email(email):
    limpar_tela()
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            select_query = "SELECT * FROM T_USER WHERE email = :email"
            cursor.execute(select_query, {'email': email})
            user = cursor.fetchone()
            if user:
                return {"email": user[1], "senha": user[2], "cpf": user[3]} 
            else:
                return None
        except oracledb.Error as e:
            print(f"Erro ao buscar o usuário no banco de dados: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def alterar_pessoal(email_antigo, email_novo, senha_nova):
    limpar_tela()
    pessoal = buscar_pessoal_por_email(email_antigo)
    if pessoal:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            try:
                update_query = """
                UPDATE T_USER 
                SET email = :email_novo, senha = :senha_nova
                WHERE email = :email_antigo
                """
                cursor.execute(update_query, {'email_novo': email_novo, 'senha_nova': senha_nova, 'email_antigo': email_antigo})
                conn.commit() 
                print("Cadastro alterado com sucesso.")
            except oracledb.Error as e:
                print(f"Erro ao alterar o cadastro no banco de dados: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Cadastro não encontrado.")
    input("\nPressione Enter para voltar ao menu...")

def remover_pessoal(email, senha):
    limpar_tela()
    if not validar_email(email):
        print("E-mail inválido! O formato correto é exemplo@dominio.com.")
        input("\nPressione enter para voltar ao menu....")
        return
    if not validar_senha(senha):
        print("Senha inválida! A senha deve ter pelo menos 8 caracteres.")
        input("\nPressione enter para voltar ao menu....")
        return
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Verificar se o e-mail existe no banco de dados
            select_query = "SELECT * FROM T_USER WHERE email = :email"
            cursor.execute(select_query, {'email': email})
            user = cursor.fetchone()

            if not user:
                print("E-mail não encontrado no sistema.")
                input("\nPressione Enter para voltar....")
                return

            # Verificar se a senha informada corresponde à senha do usuário encontrado
            if user[1] != senha:  # Supondo que a senha esteja na segunda coluna (índice 1)
                print("Senha incorreta!")
                return

            # Deletando o cadastro
            delete_query = """
            DELETE FROM T_USER WHERE email = :email AND senha = :senha
            """
            cursor.execute(delete_query, {'email': email, 'senha': senha})
            conn.commit()
            print("Cadastro removido com sucesso.")

        except oracledb.Error as e:
            print(f"Erro ao remover o usuário do banco de dados: {e}")
        finally:
            cursor.close()
            conn.close()

    input("\nPressione Enter para voltar ao menu...")


# GERENCIAMENTO DE PONTOS
def atribuir_pontos(email, pontos_a_adicionar):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT pontos FROM T_PONTOS WHERE usuario_id = (SELECT id FROM T_USER WHERE email = :email)
            """, {'email': email})
            resultado = cursor.fetchone()
            if resultado:
                pontos_atualizados = resultado[0] + pontos_a_adicionar
                cursor.execute("""
                    UPDATE T_PONTOS SET pontos = :pontos WHERE usuario_id = (SELECT id FROM T_USER WHERE email = :email)
                """, {'pontos': pontos_atualizados, 'email': email})
            else:
                cursor.execute("""
                    INSERT INTO T_PONTOS (usuario_id, pontos) 
                    VALUES ((SELECT id FROM T_USER WHERE email = :email), :pontos)
                """, {'email': email, 'pontos': pontos_a_adicionar})
            conn.commit()
            print(f"Pontos atribuídos com sucesso! {email} agora tem {pontos_a_adicionar} pontos.")
        except oracledb.Error as e:
            print(f"Erro ao atribuir pontos: {e}")
        finally:
            cursor.close()
            conn.close()
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
    atribuir_pontos(email, pontos_a_adicionar, acao_selecionada)

def atribuir_pontos(email, pontos_a_adicionar, acao_selecionada):
    usuario = buscar_pessoal_por_email(email)
    if usuario:
        if "pontos" not in usuario:
            usuario["pontos"] = 0
        usuario["pontos"] += pontos_a_adicionar  
        if "acoes" not in usuario:
            usuario["acoes"] = []
        usuario["acoes"].append({"acao": acao_selecionada, "pontos": pontos_a_adicionar}) 
        pontos[email] = usuario["pontos"]  
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
