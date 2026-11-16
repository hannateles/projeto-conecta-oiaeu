
import pytest
from werkzeug.security import generate_password_hash
import app as projeto


@pytest.fixture
def dados_voluntario():
    return {
        "nome": "Maria Silva",
        "email": "maria@email.com",
        "telefone": "11999999999",
        "formacao": "Pedagogia",
        "habilidades": "Educação",
        "disponibilidade": "Manhã",
        "senha": "senha123",
        "confirmar_senha": "senha123"
    }


def test_pagina_inicial(client):
    resposta = client.get("/")

    assert resposta.status_code == 200


def test_pagina_cadastro(client):
    resposta = client.get("/cadastro")

    assert resposta.status_code == 200


def test_cadastro_com_sucesso(
    client, monkeypatch, dados_voluntario
):
    monkeypatch.setattr(
        projeto,
        "cadastrar_voluntario",
        lambda *args: True
    )

    resposta = client.post(
        "/cadastro",
        data=dados_voluntario
    )

    assert resposta.status_code == 200
    assert b"Cadastro realizado com sucesso" in resposta.data


def test_cadastro_com_email_invalido(
    client, monkeypatch, dados_voluntario
):
    dados_voluntario["email"] = "email_invalido"

    def nao_deve_cadastrar(*args):
        pytest.fail("O cadastro nao deveria ser executado")

    monkeypatch.setattr(
        projeto,
        "cadastrar_voluntario",
        nao_deve_cadastrar
    )

    resposta = client.post(
        "/cadastro",
        data=dados_voluntario
    )

    assert resposta.status_code == 200
    assert b"Digite um e-mail valido." in resposta.data


def test_cadastro_com_senha_diferente(
    client, monkeypatch, dados_voluntario
):
    dados_voluntario["confirmar_senha"] = "outraSenha123"

    monkeypatch.setattr(
        projeto,
        "cadastrar_voluntario",
        lambda *args: pytest.fail("Nao deveria cadastrar")
    )

    resposta = client.post(
        "/cadastro",
        data=dados_voluntario
    )

    assert b"As senhas nao coincidem!" in resposta.data


def test_login_voluntario_com_sucesso(
    client, monkeypatch
):
    senha_hash = generate_password_hash("senha123")

    monkeypatch.setattr(
        projeto,
        "buscar_voluntario",
        lambda email: (1, "Maria", email, senha_hash)
    )

    resposta = client.post(
        "/login",
        data={
            "email": "maria@email.com",
            "senha": "senha123",
            "tipo_usuario": "voluntario"
        }
    )

    assert resposta.status_code == 302
    assert resposta.location.endswith("/vagas")


def test_login_com_senha_incorreta(
    client, monkeypatch
):
    senha_hash = generate_password_hash("senha123")

    monkeypatch.setattr(
        projeto,
        "buscar_voluntario",
        lambda email: (1, "Maria", email, senha_hash)
    )

    resposta = client.post(
        "/login",
        data={
            "email": "maria@email.com",
            "senha": "senhaerrada",
            "tipo_usuario": "voluntario"
        }
    )

    assert resposta.status_code == 200
    assert b"E-mail ou senha incorretos." in resposta.data


def test_voluntario_nao_acessa_painel(client):
    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "voluntario"

    resposta = client.get("/painel")

    assert resposta.status_code == 302
    assert resposta.location.endswith("/login")


def test_administrador_acessa_painel(
    client, monkeypatch
):
    monkeypatch.setattr(
        projeto,
        "obter_resumo_admin",
        lambda: {
            "voluntarios": 5,
            "vagas": 3,
            "inscricoes": 8,
            "pendentes": 2,
            "aprovados": 4
        }
    )

    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "administrador"

    resposta = client.get("/painel")

    assert resposta.status_code == 200


def test_voluntario_visualiza_somente_vagas_abertas(
    client, monkeypatch
):
    vagas = [
        (1, "Aula de reforco", "", "", "", "", "aberta"),
        (2, "Evento encerrado", "", "", "", "", "encerrada")
    ]

    monkeypatch.setattr(
        projeto,
        "listar_vagas",
        lambda: vagas
    )

    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "voluntario"

    resposta = client.get("/vagas")

    assert resposta.status_code == 200
    assert b"Aula de reforco" in resposta.data
    assert b"Evento encerrado" not in resposta.data


def test_voluntario_realiza_inscricao(
    client, monkeypatch
):
    chamadas = []

    def simular_inscricao(id_voluntario, id_vaga):
        chamadas.append((id_voluntario, id_vaga))
        return True

    monkeypatch.setattr(
        projeto,
        "inscrever_voluntario",
        simular_inscricao
    )

    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "voluntario"

    resposta = client.post("/inscrever/10")

    assert resposta.status_code == 302
    assert chamadas == [(1, 10)]


def test_inscricao_duplicada(
    client, monkeypatch
):
    monkeypatch.setattr(
        projeto,
        "inscrever_voluntario",
        lambda *args: (_ for _ in ()).throw(
            projeto.pyodbc.IntegrityError("Inscricao duplicada")
        )
    )

    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "voluntario"

    resposta = client.post("/inscrever/10")

    assert resposta.status_code == 302
    assert "mensagem=duplicada" in resposta.location


def test_administrador_nao_pode_ser_acessado_por_voluntario(
    client
):
    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "voluntario"

    resposta = client.get("/inscricoes")

    assert resposta.status_code == 302
    assert resposta.location.endswith("/login")


def test_logout(client):
    with client.session_transaction() as sess:
        sess["id_usuario"] = 1
        sess["tipo_usuario"] = "voluntario"

    resposta = client.get("/sair")

    assert resposta.status_code == 302

    with client.session_transaction() as sess:
        assert "id_usuario" not in sess
        assert "tipo_usuario" not in sess
