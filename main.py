import json
import re
import oracledb
import os 
import os
os.system('cls' if os.name == 'nt' else 'clear')

def conectar():
    username = 'rm557591'
    password = 'fiap24'
    cs = "oracle.fiap.com.br:1521/orcl"
    
    try:
        # Conectando ao banco de dados
        conn = oracledb.connect(user=username, password=password, dsn=cs)
        return conn
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Erro ao conectar ao banco de dados:")
        print(f"Código do erro: {error.code}")
        print(f"Mensagem do erro: {error.message}")
        return None

# Conectar ao banco
conexao = conectar()

if conexao:
    try:
        # Criando o cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Comando SQL para criar a tabela
        sql_criar_tabela = """
        CREATE TABLE IF NOT EXISTS T_usuarios (
            cpf VARCHAR2(11) PRIMARY KEY,
            nome VARCHAR2(100),
            senha VARCHAR2(100)
        )
        """
        
        # Executando o comando SQL
        cursor.execute(sql_criar_tabela)
        
        # Confirmando as mudanças no banco de dados (commit)
        conexao.commit()
        
        print("Tabela 'T_usuarios' criada com sucesso!")
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Erro ao executar o comando SQL:")
        print(f"Código do erro: {error.code}")
        print(f"Mensagem do erro: {error.message}")
    
    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

# Funções de Validação
def validar_email(email):
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True
    print("Erro: Email inválido.")
    return False

def validar_senha(senha):
    if len(senha) < 8:
        print("Erro: A senha deve ter no mínimo 8 caracteres.")
        return False
    if not re.search(r'[A-Z]', senha):
        print("Erro: A senha deve conter pelo menos uma letra maiúscula.")
        return False
    if not re.search(r'[a-z]', senha):
        print("Erro: A senha deve conter pelo menos uma letra minúscula.")
        return False
    if not re.search(r'\d', senha):
        print("Erro: A senha deve conter pelo menos um número.")
        return False
    return True

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        print("Erro: CPF deve ter 11 dígitos.")
        return False
    if cpf == cpf[0] * 11:
        print("Erro: CPF inválido.")
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * (i + 1 - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            print("Erro: CPF inválido.")
            return False
    return True

# Função CRUD para Cadastro de Usuários
def cadastrar_usuario():
    while True:
        print("\n--- Cadastro de Usuários ---")
        print("1. Novo cadastro de usuário")
        print("2. Listar todos os usuários")
        print("3. Atualizar usuário")
        print("4. Excluir usuário")
        print("5. Voltar")

        opcao = input("Opção: ")
        
        if opcao == "1":
            email = input("Email: ")
            senha = input("Senha: ")
            cpf = input("CPF: ")
            if validar_email(email) and validar_senha(senha) and validar_cpf(cpf):
                conn = conectar()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO usuarios (email, senha, cpf) VALUES (:1, :2, :3)", (email, senha, cpf))
                        conn.commit()
                        print("Usuário cadastrado com sucesso!")
                    except oracledb.DatabaseError as e:
                        error, = e.args
                        print("Erro ao cadastrar usuário:", error.message)
                    finally:
                        conn.close()

        elif opcao == "2":
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM usuarios")
                    for user in cursor:
                        print(f"ID: {user[0]}, Email: {user[1]}, CPF: {user[3]}")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print("Erro ao listar usuários:", error.message)
                finally:
                    conn.close()

        elif opcao == "3":
            id = int(input("ID do usuário a atualizar: "))
            novo_email = input("Novo email (deixe em branco para não alterar): ")
            nova_senha = input("Nova senha (deixe em branco para não alterar): ")
            novo_cpf = input("Novo CPF (deixe em branco para não alterar): ")
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    if novo_email and validar_email(novo_email):
                        cursor.execute("UPDATE usuarios SET email = :1 WHERE id = :2", (novo_email, id))
                    if nova_senha and validar_senha(nova_senha):
                        cursor.execute("UPDATE usuarios SET senha = :1 WHERE id = :2", (nova_senha, id))
                    if novo_cpf and validar_cpf(novo_cpf):
                        cursor.execute("UPDATE usuarios SET cpf = :1 WHERE id = :2", (novo_cpf, id))
                    conn.commit()
                    print("Usuário atualizado com sucesso!")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print("Erro ao atualizar usuário:", error.message)
                finally:
                    conn.close()
                    
# precisa de ajustes
        elif opcao == "4":
            id = int(input("ID do usuário a excluir: "))
            conn = conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM usuarios WHERE id = :1", [id])
                    conn.commit()
                    print("Usuário excluído com sucesso!")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print("Erro ao excluir usuário:", error.message)
                finally:
                    conn.close()

        elif opcao == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

# Função para Gerenciar Pontos
def gerenciar_pontos():
    print("Funcionalidade de Gerenciamento de Pontos em desenvolvimento...")

# Função para Relatar Problemas
def relatar_problema():
    problema = input("Descreva o problema: ")
    print("Problema relatado com sucesso.")

# Função para Exportar Dados para JSON
def exportar_json():
    dados = {"example": "data"}
    with open("dados_exportados.json", "w") as arquivo:
        json.dump(dados, arquivo)
    print("Dados exportados para JSON com sucesso.")

# Função Principal para Exibir o Menu
def menu_principal():
    while True:
        print("\nMenu Principal:")
        print("1 - Cadastro de Usuários")
        print("2 - Gerenciar Sistemas de Pontos")
        print("3 - Relatar Problema ")
        print("4 - Exportar para JSON")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            gerenciar_pontos()
        elif opcao == "3":
            relatar_problema()
        elif opcao == "4":
            exportar_json()
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o Menu Principal
menu_principal()
