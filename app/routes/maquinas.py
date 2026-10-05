from flask import Blueprint, jsonify
from app.database.database import get_db

maquinas_bp=Blueprint("maquinas",__name__)

@maquinas_bp.get("/maquinas")
def listar_maquinas():
    connection=get_db()
    maquinas=connection.execute("SELECT id,codigo,nome,local,status FROM maquinas ORDER BY codigo").fetchall()
    connection.close()
    return jsonify([dict(maquina) for maquina in maquinas])

@maquinas_bp.get("/maquinas/<int:maquina_id>")
def consultar_maquina(maquina_id):
    connection=get_db()
    maquina=connection.execute("SELECT id,codigo,nome,local,status FROM maquinas WHERE id=?",(maquina_id,)).fetchone()
    connection.close()
    if not maquina:
        return jsonify({"erro":"Máquina não encontrada"}),404
    return jsonify(dict(maquina))
