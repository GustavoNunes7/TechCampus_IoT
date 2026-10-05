from functools import wraps
from flask import Blueprint, current_app, jsonify, request
from app.database.database import get_db
from app.services.estoque_service import retirar_unidade
from app.services.retirada_service import agora_iso
from app.services.token_service import token_expirado

iot_bp=Blueprint("iot",__name__)

def exigir_api_key(view):
    @wraps(view)
    def wrapper(*args,**kwargs):
        chave=request.headers.get("X-IoT-Key")
        if not chave or chave!=current_app.config["IOT_API_KEY"]:
            return jsonify({"autorizado":False,"erro":"Chave da máquina inválida"}),401
        return view(*args,**kwargs)
    return wrapper

@iot_bp.post("/iot/validar-token")
@exigir_api_key
def validar_token():
    dados=request.get_json(silent=True) or {}
    token=str(dados.get("token","")).strip()
    maquina_codigo=str(dados.get("maquina","")).strip()
    if not token or not maquina_codigo:
        return jsonify({"autorizado":False,"motivo":"token e maquina são obrigatórios"}),400

    connection=get_db()
    registro=connection.execute("""SELECT t.id AS token_id,t.token,t.usuario_id,t.material_id,
        t.maquina_id,t.expira_em,t.status,m.nome AS material
        FROM tokens t JOIN materiais m ON m.id=t.material_id WHERE t.token=?""",(token,)).fetchone()

    if not registro:
        connection.close()
        return jsonify({"autorizado":False,"motivo":"Token não encontrado"}),404
    if registro["status"]!="disponivel":
        connection.close()
        return jsonify({"autorizado":False,"motivo":f"Token {registro['status']}"}),409
    if token_expirado(registro["expira_em"]):
        connection.execute("UPDATE tokens SET status='expirado' WHERE id=?",(registro["token_id"],))
        connection.commit(); connection.close()
        return jsonify({"autorizado":False,"motivo":"Token expirado"}),409

    maquina=connection.execute("SELECT id,codigo,status FROM maquinas WHERE codigo=?",(maquina_codigo,)).fetchone()
    if not maquina:
        connection.close()
        return jsonify({"autorizado":False,"motivo":"Máquina não encontrada"}),404
    if maquina["status"]!="online":
        connection.close()
        return jsonify({"autorizado":False,"motivo":"Máquina indisponível"}),409
    if registro["maquina_id"] is not None and registro["maquina_id"]!=maquina["id"]:
        connection.close()
        return jsonify({"autorizado":False,"motivo":"Token não pertence a esta máquina"}),403

    material=connection.execute("SELECT quantidade,ativo FROM materiais WHERE id=?",(registro["material_id"],)).fetchone()
    if not material or not material["ativo"] or material["quantidade"]<=0:
        connection.close()
        return jsonify({"autorizado":False,"motivo":"Material indisponível ou sem estoque"}),409
    connection.close()
    return jsonify({"autorizado":True,"token":registro["token"],"material":registro["material"],
                    "material_id":registro["material_id"],"aluno_id":registro["usuario_id"],
                    "maquina":maquina["codigo"]})

@iot_bp.post("/iot/retirada")
@exigir_api_key
def registrar_retirada():
    dados=request.get_json(silent=True) or {}
    token=str(dados.get("token","")).strip()
    maquina_codigo=str(dados.get("maquina","")).strip()
    if not token or not maquina_codigo:
        return jsonify({"sucesso":False,"erro":"token e maquina são obrigatórios"}),400

    connection=get_db()
    registro=connection.execute("""SELECT t.id AS token_id,t.usuario_id,t.material_id,t.maquina_id,
        t.expira_em,t.status,ma.id AS maquina_real_id
        FROM tokens t LEFT JOIN maquinas ma ON ma.codigo=? WHERE t.token=?""",(maquina_codigo,token)).fetchone()

    if not registro:
        connection.close(); return jsonify({"sucesso":False,"erro":"Token não encontrado"}),404
    if registro["status"]!="disponivel":
        connection.close(); return jsonify({"sucesso":False,"erro":f"Token {registro['status']}"}),409
    if registro["maquina_real_id"] is None:
        connection.close(); return jsonify({"sucesso":False,"erro":"Máquina não encontrada"}),404
    if registro["maquina_id"] is not None and registro["maquina_id"]!=registro["maquina_real_id"]:
        connection.close(); return jsonify({"sucesso":False,"erro":"Token não pertence a esta máquina"}),403
    if token_expirado(registro["expira_em"]):
        connection.execute("UPDATE tokens SET status='expirado' WHERE id=?",(registro["token_id"],))
        connection.commit(); connection.close()
        return jsonify({"sucesso":False,"erro":"Token expirado"}),409
    if not retirar_unidade(connection,registro["material_id"]):
        connection.rollback(); connection.close()
        return jsonify({"sucesso":False,"erro":"Material sem estoque"}),409

    connection.execute("""INSERT INTO retiradas
        (token_id,usuario_id,material_id,maquina_id,data_hora,status)
        VALUES (?,?,?,?,?,'concluida')""",
        (registro["token_id"],registro["usuario_id"],registro["material_id"],
         registro["maquina_real_id"],agora_iso()))
    connection.execute("UPDATE tokens SET status='utilizado' WHERE id=?",(registro["token_id"],))
    connection.commit(); connection.close()
    return jsonify({"sucesso":True,"mensagem":"Retirada registrada com sucesso"})
