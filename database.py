
import pyodbc
from werkzeug.security import generate_password_hash


# ============================================
# CONEXAO COM SQL SERVER
# ============================================

def conectar_banco():

    try:

        conexao = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=CONECTA_OIAEU;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=5;"
        )

        return conexao

    except pyodbc.Error as erro:

        print("Erro ao conectar com o banco:")
        print(erro)

        return None


# ============================================
# CADASTRAR VOLUNTARIO
# ============================================

def cadastrar_voluntario(
    nome,
    email,
    telefone,
    formacao,
    habilidades,
    disponibilidade,
    senha
):

    conexao = conectar_banco()

    if conexao is None:
        return False

    cursor = None

    try:

        senha_hash = generate_password_hash(senha)

        cursor = conexao.cursor()

        comando = """
            INSERT INTO Voluntario
            (
                nome,
                email,
                telefone,
                formacao,
                habilidades,
                disponibilidade,
                senha_hash
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            comando,
            nome,
            email,
            telefone,
            formacao,
            habilidades,
            disponibilidade,
            senha_hash
        )

        conexao.commit()

        return True

    except pyodbc.Error:

        conexao.rollback()
        raise

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# BUSCAR VOLUNTARIO PARA LOGIN
# ============================================

def buscar_voluntario(email):

    conexao = conectar_banco()

    if conexao is None:
        raise ConnectionError("Não foi possível conectar ao banco.")

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id_voluntario,
                nome,
                email,
                senha_hash
            FROM Voluntario
            WHERE email = ?
            AND ativo = 1
        """, email)

        return cursor.fetchone()

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# BUSCAR ADMINISTRADOR PARA LOGIN
# ============================================

def buscar_administrador(email):

    conexao = conectar_banco()

    if conexao is None:
        raise ConnectionError("Não foi possível conectar ao banco.")

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id_administrador,
                nome,
                email,
                senha_hash
            FROM Administrador
            WHERE email = ?
            AND ativo = 1
        """, email)

        return cursor.fetchone()

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# CADASTRAR NOVA VAGA
# ============================================

def cadastrar_vaga(
    titulo,
    descricao,
    area_atuacao,
    requisitos
):

    conexao = conectar_banco()

    if conexao is None:
        return False

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO Vaga
            (
                titulo,
                descricao,
                area_atuacao,
                requisitos,
                status
            )
            VALUES (?, ?, ?, ?, 'aberta')
        """,
            titulo,
            descricao,
            area_atuacao,
            requisitos
        )

        conexao.commit()

        return True

    except pyodbc.Error:

        conexao.rollback()
        raise

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# LISTAR TODAS AS VAGAS
# ============================================

def listar_vagas():

    conexao = conectar_banco()

    if conexao is None:
        return None

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id_vaga,
                titulo,
                descricao,
                area_atuacao,
                requisitos,
                data_publicacao,
                status
            FROM Vaga
            ORDER BY data_publicacao DESC
        """)

        return cursor.fetchall()

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# ATIVAR OU DESATIVAR VAGA
# ============================================

def atualizar_status_vaga(id_vaga, novo_status):

    if novo_status not in ["aberta", "encerrada"]:
        return False

    conexao = conectar_banco()

    if conexao is None:
        return False

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE Vaga
            SET status = ?
            WHERE id_vaga = ?
        """, novo_status, id_vaga)

        if cursor.rowcount == 0:

            conexao.rollback()
            return False

        conexao.commit()

        return True

    except pyodbc.Error:

        conexao.rollback()
        raise

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# INSCRICAO DO VOLUNTARIO
# ============================================

def inscrever_voluntario(id_voluntario, id_vaga):

    conexao = conectar_banco()

    if conexao is None:
        return False

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO Inscricao
            (
                id_voluntario,
                id_vaga,
                status
            )
            SELECT ?, ?, 'pendente'
            WHERE EXISTS (
                SELECT 1
                FROM Vaga
                WHERE id_vaga = ?
                AND status = 'aberta'
            )
            AND EXISTS (
                SELECT 1
                FROM Voluntario
                WHERE id_voluntario = ?
                AND ativo = 1
            )
        """,
            id_voluntario,
            id_vaga,
            id_vaga,
            id_voluntario
        )

        if cursor.rowcount == 0:

            conexao.rollback()
            return False

        conexao.commit()

        return True

    except pyodbc.IntegrityError:

        conexao.rollback()
        raise

    except pyodbc.Error:

        conexao.rollback()
        raise

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# LISTAR INSCRICOES
# SOMENTE PARA O ADMINISTRADOR
# ============================================

def listar_inscricoes():

    conexao = conectar_banco()

    if conexao is None:
        raise ConnectionError("Não foi possível conectar ao banco.")

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                Inscricao.id_inscricao,
                Voluntario.id_voluntario,
                Voluntario.nome,
                Voluntario.email,
                Voluntario.telefone,
                Voluntario.formacao,
                Voluntario.habilidades,
                Vaga.titulo,
                Inscricao.status,
                Inscricao.data_inscricao,
                Vaga.id_vaga,
                Vaga.area_atuacao
            FROM Inscricao

            INNER JOIN Voluntario
                ON Inscricao.id_voluntario =
                   Voluntario.id_voluntario

            INNER JOIN Vaga
                ON Inscricao.id_vaga =
                   Vaga.id_vaga

            ORDER BY
                CASE Inscricao.status
                    WHEN 'pendente' THEN 1
                    WHEN 'aprovado' THEN 2
                    WHEN 'recusado' THEN 3
                END,
                Inscricao.data_inscricao DESC
        """)

        return cursor.fetchall()

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# ATUALIZAR STATUS DA INSCRICAO
# SOMENTE PARA O ADMINISTRADOR
# ============================================

def atualizar_status_inscricao(id_inscricao, novo_status):

    if novo_status not in ["aprovado", "recusado"]:
        return False

    conexao = conectar_banco()

    if conexao is None:
        return False

    cursor = None

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE Inscricao
            SET status = ?
            WHERE id_inscricao = ?
            AND status = 'pendente'
        """,
            novo_status,
            id_inscricao
        )

        if cursor.rowcount == 0:

            conexao.rollback()
            return False

        conexao.commit()

        return True

    except pyodbc.Error:

        conexao.rollback()
        raise

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# RESUMO DO PAINEL ADMINISTRATIVO
# ============================================

def obter_resumo_admin():

    conexao = conectar_banco()

    if conexao is None:
        return None

    cursor = None

    try:

        cursor = conexao.cursor()

        resumo = {}

        # VOLUNTARIOS ATIVOS

        cursor.execute("""
            SELECT COUNT(*)
            FROM Voluntario
            WHERE ativo = 1
        """)

        resumo["voluntarios"] = cursor.fetchone()[0]

        # TOTAL DE VAGAS

        cursor.execute("""
            SELECT COUNT(*)
            FROM Vaga
        """)

        resumo["vagas"] = cursor.fetchone()[0]

        # TOTAL DE INSCRICOES

        cursor.execute("""
            SELECT COUNT(*)
            FROM Inscricao
        """)

        resumo["inscricoes"] = cursor.fetchone()[0]

        # INSCRICOES PENDENTES

        cursor.execute("""
            SELECT COUNT(*)
            FROM Inscricao
            WHERE status = 'pendente'
        """)

        resumo["pendentes"] = cursor.fetchone()[0]

        # INSCRICOES APROVADAS

        cursor.execute("""
            SELECT COUNT(*)
            FROM Inscricao
            WHERE status = 'aprovado'
        """)

        resumo["aprovados"] = cursor.fetchone()[0]

        return resumo

    finally:

        if cursor:
            cursor.close()

        conexao.close()


# ============================================
# TESTAR CONEXAO
# ============================================

if __name__ == "__main__":

    conexao = conectar_banco()

    if conexao:

        print("Conexão realizada com sucesso! ❤️")

        conexao.close()

        print("Conexão encerrada.")

    else:

        print("Não foi possível conectar ao banco.")
