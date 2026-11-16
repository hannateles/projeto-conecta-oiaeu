
import database


def test_nao_permite_status_invalido_de_vaga(monkeypatch):
    def nao_deve_conectar():
        raise AssertionError("Nao deveria acessar o banco")

    monkeypatch.setattr(database, "conectar_banco", nao_deve_conectar)

    resultado = database.atualizar_status_vaga(
        1, "invalida"
    )

    assert resultado is False


def test_nao_permite_status_invalido_de_inscricao(monkeypatch):
    def nao_deve_conectar():
        raise AssertionError("Nao deveria acessar o banco")

    monkeypatch.setattr(database, "conectar_banco", nao_deve_conectar)

    resultado = database.atualizar_status_inscricao(
        1, "pendente"
    )

    assert resultado is False


def test_nao_permite_cadastrar_vaga_sem_conexao(monkeypatch):
    monkeypatch.setattr(
        database,
        "conectar_banco",
        lambda: None
    )

    resultado = database.cadastrar_vaga(
        "Voluntariado",
        "Descricao",
        "Educacao",
        "Disponibilidade"
    )

    assert resultado is False
