
from werkzeug.security import generate_password_hash
from database import conectar_banco

conexao = conectar_banco()

if conexao:
    cursor = conexao.cursor()

    senha_hash = generate_password_hash("123")

    cursor.execute("""
        INSERT INTO Administrador (nome, email, senha_hash)
        VALUES (?, ?, ?)
    """, "Administrador OIAEU", "admin@oiaeu.org.br", senha_hash)

    conexao.commit()

    cursor.close()
    conexao.close()

    print("Administrador cadastrado com sucesso!")
