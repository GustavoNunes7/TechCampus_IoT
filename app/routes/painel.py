from flask import Blueprint, render_template

painel_bp = Blueprint("painel", __name__)

@painel_bp.get("/")
def dashboard():
    return render_template("dashboard.html")

@painel_bp.get("/tokens")
def tokens():
    return render_template("tokens.html")

@painel_bp.get("/estoque")
def estoque():
    return render_template("estoque.html")

@painel_bp.get("/maquinas")
def maquinas():
    return render_template("maquinas.html")

@painel_bp.get("/solicitacoes")
def solicitacoes():
    return render_template("solicitacoes.html")
