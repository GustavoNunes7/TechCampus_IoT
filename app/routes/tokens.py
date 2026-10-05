from flask import Blueprint, jsonify
from app.database.database import get_db
from app.services.token_service import token_expirado

tokens_bp=Blueprint("tokens",__name__)

@tokens_bp.get("/tokens/<token>")
def consultar_token(token):
    connection=get_db()
    registro=connection.execute("""SELECT t.id,t.token,t.usuario_id,t.material_id,
        t.maquina_id,t.criado_em,t.expira_em,t.status,m.nome AS material
        FROM tokens t JOIN materiais m ON m.id=t.material_id WHERE t.token=?""",(token,)).fetchone()
    if not registro:
        connection.close()
        return jsonify({"erro":"Token não encontrado"}),404

    status=registro["status"]
    if status=="disponivel" and token_expirado(registro["expira_em"]):
        connection.execute("UPDATE tokens SET status='expirado' WHERE id=?",(registro["id"],))
        connection.commit()
        status="expirado"
    connection.close()
    return jsonify({
        "token":registro["token"],"status":status,"aluno_id":registro["usuario_id"],
        "material_id":registro["material_id"],"material":registro["material"],
        "maquina_id":registro["maquina_id"],"criado_em":registro["criado_em"],
        "expira_em":registro["expira_em"]
    })
