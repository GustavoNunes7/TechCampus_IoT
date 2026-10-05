from flask import Blueprint, jsonify
from app.database.database import get_db

estoque_bp=Blueprint("estoque",__name__)

@estoque_bp.get("/estoque")
def listar_estoque():
    connection=get_db()
    materiais=connection.execute("SELECT id,nome,descricao,quantidade,ativo FROM materiais ORDER BY nome").fetchall()
    connection.close()
    return jsonify([dict(item) for item in materiais])

@estoque_bp.get("/estoque/<int:material_id>")
def consultar_material(material_id):
    connection=get_db()
    material=connection.execute("SELECT id,nome,descricao,quantidade,ativo FROM materiais WHERE id=?",(material_id,)).fetchone()
    connection.close()
    if not material:
        return jsonify({"erro":"Material não encontrado"}),404
    return jsonify(dict(material))
