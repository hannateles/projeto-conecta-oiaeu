
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import check_password_hash

import pyodbc
import re
import os

from database import (
    cadastrar_voluntario,
    buscar_voluntario,
    buscar_administrador,
    cadastrar_vaga,
    listar_vagas,
    atualizar_status_vaga,
    inscrever_voluntario,
    obter_resumo_admin,
    listar_inscricoes,
    atualizar_status_inscricao
)


# ============================================
# CONFIGURACAO FLASK
# ============================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "chave-temporaria-conecta-oiaeu"
)


# ============================================
# PAGINA INICIAL
# ============================================

@app.route("/")
def inicio():

    return render_template("index.html")


# ============================================
# CADASTRO DE VOLUNTARIO
# ============================================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        formacao = request.form.get("formacao", "").strip()
        habilidades = request.form.get("habilidades", "").strip()
        disponibilidade = request.form.get("disponibilidade", "").strip()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        if not all([
            nome,
            email,
            telefone,
            formacao,
            habilidades,
            disponibilidade,
            senha,
            confirmar_senha
        ]):

            return render_template(
                "cadastro.html",
                erro="Preencha todos os campos!"
            )

        email_regex = r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(email_regex, email):

            return render_template(
                "cadastro.html",
                erro="Digite um e-mail válido."
            )

        numero = re.sub(r"\D", "", telefone)

        if len(numero) not in [10, 11]:

            return render_template(
                "cadastro.html",
                erro="Telefone inválido! Digite DDD e número completo."
            )

        if len(senha) < 8:

            return render_template(
                "cadastro.html",
                erro="A senha deve possuir pelo menos 8 caracteres."
            )

        if senha != confirmar_senha:

            return render_template(
                "cadastro.html",
                erro="As senhas não coincidem!"
            )

        try:

            resultado = cadastrar_voluntario(
                nome,
                email,
                telefone,
                formacao,
                habilidades,
                disponibilidade,
                senha
            )

            if resultado:

                return render_template(
                    "cadastro.html",
                    sucesso="Cadastro realizado com sucesso! ❤️"
                )

            return render_template(
                "cadastro.html",
                erro="Não foi possível conectar ao banco."
            )

        except pyodbc.IntegrityError:

            return render_template(
                "cadastro.html",
                erro="Este e-mail já possui cadastro!"
            )

        except (pyodbc.Error, ConnectionError) as erro:

            print("Erro no cadastro:", erro)

            return render_template(
                "cadastro.html",
                erro="Ocorreu um erro ao realizar o cadastro."
            )

    return render_template("cadastro.html")


# ============================================
# LOGIN ADMINISTRADOR E VOLUNTARIO
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        tipo_usuario = request.form.get(
            "tipo_usuario",
            "voluntario"
        )

        if tipo_usuario not in ["administrador", "voluntario"]:

            return render_template(
                "login.html",
                erro="Tipo de acesso inválido."
            )

        if not email or not senha:

            return render_template(
                "login.html",
                erro="Preencha o e-mail e a senha."
            )

        try:

            if tipo_usuario == "administrador":

                usuario = buscar_administrador(email)

                if usuario and check_password_hash(
                    usuario[3],
                    senha
                ):

                    session.clear()

                    session["id_usuario"] = usuario[0]
                    session["nome_usuario"] = usuario[1]
                    session["tipo_usuario"] = "administrador"

                    return redirect(url_for("painel"))

            else:

                usuario = buscar_voluntario(email)

                if usuario and check_password_hash(
                    usuario[3],
                    senha
                ):

                    session.clear()

                    session["id_usuario"] = usuario[0]
                    session["nome_usuario"] = usuario[1]
                    session["tipo_usuario"] = "voluntario"

                    return redirect(url_for("vagas"))

            return render_template(
                "login.html",
                erro="E-mail ou senha incorretos."
            )

        except (pyodbc.Error, ConnectionError) as erro:

            print("Erro no login:", erro)

            return render_template(
                "login.html",
                erro="Não foi possível realizar o login."
            )

    return render_template("login.html")


# ============================================
# SAIR DA CONTA
# ============================================

@app.route("/sair")
def sair():

    session.clear()

    return redirect(url_for("inicio"))


# ============================================
# PAINEL ADMINISTRATIVO
# ============================================

@app.route("/painel")
def painel():

    if session.get("tipo_usuario") != "administrador":

        return redirect(url_for("login"))

    try:

        resumo = obter_resumo_admin()

        if resumo is None:

            return "Erro ao conectar ao banco.", 500

        return render_template(
            "painel.html",
            resumo=resumo
        )

    except (pyodbc.Error, ConnectionError) as erro:

        print("Erro no painel:", erro)

        return "Erro ao carregar o painel.", 500


# ============================================
# CADASTRAR NOVA VAGA
# ============================================

@app.route("/cadastrar-vaga", methods=["GET", "POST"])
def cadastrar_vaga_rota():

    if session.get("tipo_usuario") != "administrador":

        return redirect(url_for("login"))

    if request.method == "POST":

        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        area_atuacao = request.form.get("area_atuacao", "").strip()
        requisitos = request.form.get("requisitos", "").strip()

        if not all([
            titulo,
            descricao,
            area_atuacao,
            requisitos
        ]):

            return render_template(
                "cadastrar_vaga.html",
                erro="Preencha todos os campos!"
            )

        try:

            resultado = cadastrar_vaga(
                titulo,
                descricao,
                area_atuacao,
                requisitos
            )

            if resultado:

                return redirect(url_for("vagas"))

            return render_template(
                "cadastrar_vaga.html",
                erro="Não foi possível cadastrar a vaga."
            )

        except pyodbc.Error as erro:

            print("Erro ao cadastrar vaga:", erro)

            return render_template(
                "cadastrar_vaga.html",
                erro="Ocorreu um erro ao cadastrar a vaga."
            )

    return render_template("cadastrar_vaga.html")


# ============================================
# VISUALIZAR VAGAS
# ADMINISTRADOR E VOLUNTARIO
# ============================================

@app.route("/vagas")
def vagas():

    tipo_usuario = session.get("tipo_usuario")

    if tipo_usuario not in ["administrador", "voluntario"]:

        return redirect(url_for("login"))

    try:

        todas_vagas = listar_vagas()

        if todas_vagas is None:

            return "Erro ao conectar ao banco.", 500

        if tipo_usuario == "voluntario":

            todas_vagas = [
                vaga for vaga in todas_vagas
                if vaga[6] == "aberta"
            ]

        return render_template(
            "vagas.html",
            vagas=todas_vagas,
            tipo_usuario=tipo_usuario
        )

    except (pyodbc.Error, ConnectionError) as erro:

        print("Erro ao consultar vagas:", erro)

        return "Erro ao consultar as vagas.", 500


# ============================================
# ATIVAR OU DESATIVAR VAGA
# SOMENTE ADMINISTRADOR
# ============================================

@app.route(
    "/alterar-status-vaga/<int:id_vaga>",
    methods=["POST"]
)
def alterar_status_vaga(id_vaga):

    if session.get("tipo_usuario") != "administrador":

        return redirect(url_for("login"))

    novo_status = request.form.get("status")

    if novo_status not in ["aberta", "encerrada"]:

        return redirect(url_for("vagas"))

    try:

        atualizar_status_vaga(
            id_vaga,
            novo_status
        )

        return redirect(url_for("vagas"))

    except (pyodbc.Error, ConnectionError) as erro:

        print("Erro ao alterar status:", erro)

        return "Erro ao atualizar a vaga.", 500


# ============================================
# VOLUNTARIO SE INSCREVER NA VAGA
# ============================================

@app.route(
    "/inscrever/<int:id_vaga>",
    methods=["POST"]
)
def realizar_inscricao(id_vaga):

    if session.get("tipo_usuario") != "voluntario":

        return redirect(url_for("login"))

    id_voluntario = session.get("id_usuario")

    try:

        resultado = inscrever_voluntario(
            id_voluntario,
            id_vaga
        )

        if resultado:

            return redirect(
                url_for("vagas", mensagem="sucesso")
            )

        return redirect(
            url_for("vagas", mensagem="indisponivel")
        )

    except pyodbc.IntegrityError:

        return redirect(
            url_for("vagas", mensagem="duplicada")
        )

    except (pyodbc.Error, ConnectionError) as erro:

        print("Erro ao realizar inscrição:", erro)

        return "Erro ao realizar inscrição.", 500


# ============================================
# GERENCIAR INSCRICOES
# SOMENTE ADMINISTRADOR
# ============================================

@app.route("/inscricoes")
def inscricoes():

    if session.get("tipo_usuario") != "administrador":

        return redirect(url_for("login"))

    try:

        todas_inscricoes = listar_inscricoes()

        total_pendentes = sum(
            1 for inscricao in todas_inscricoes
            if inscricao[8] == "pendente"
        )

        total_aprovadas = sum(
            1 for inscricao in todas_inscricoes
            if inscricao[8] == "aprovado"
        )

        total_recusadas = sum(
            1 for inscricao in todas_inscricoes
            if inscricao[8] == "recusado"
        )

        return render_template(
            "inscricoes.html",
            inscricoes=todas_inscricoes,
            total_inscricoes=len(todas_inscricoes),
            total_pendentes=total_pendentes,
            total_aprovadas=total_aprovadas,
            total_recusadas=total_recusadas
        )

    except (pyodbc.Error, ConnectionError) as erro:

        print("Erro ao consultar inscrições:", erro)

        return "Erro ao carregar as inscrições.", 500


# ============================================
# APROVAR OU RECUSAR INSCRICAO
# SOMENTE ADMINISTRADOR
# ============================================

@app.route(
    "/alterar-status-inscricao/<int:id_inscricao>",
    methods=["POST"]
)
def alterar_status_inscricao(id_inscricao):

    if session.get("tipo_usuario") != "administrador":

        return redirect(url_for("login"))

    novo_status = request.form.get("status")

    if novo_status not in ["aprovado", "recusado"]:

        return redirect(url_for("inscricoes"))

    try:

        resultado = atualizar_status_inscricao(
            id_inscricao,
            novo_status
        )

        if resultado:

            return redirect(
                url_for(
                    "inscricoes",
                    mensagem="atualizada"
                )
            )

        return redirect(
            url_for(
                "inscricoes",
                mensagem="indisponivel"
            )
        )

    except (pyodbc.Error, ConnectionError) as erro:

        print("Erro ao atualizar inscrição:", erro)

        return "Erro ao atualizar a inscrição.", 500


# ============================================
# EXECUTAR APLICACAO
# ============================================

if __name__ == "__main__":

    app.run(debug=True)
