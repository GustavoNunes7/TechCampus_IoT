from flask import Blueprint, jsonify, request
from app.database.database import get_db
from app.services.token_service import criar_validade, gerar_token, agora_utc

solicitacoes_bp=Blueprint("solicitacoes",__name__)

@solicitacoes_bp.post("/solicitacoes")
def criar_solicitacao():
    dados=request.get_json(silent=True) or {}
    usuario_id=dados.get("aluno_id")
    material_id=dados.get("material_id")
    maquina_id=dados.get("maquina_id")

    if not usuario_id or not material_id:
        return jsonify({"erro":"aluno_id e material_id são obrigatórios"}),400

    connection=get_db()
    usuario=connection.execute("SELECT id,nome,ativo FROM usuarios WHERE id=?",(usuario_id,)).fetchone()
    if not usuario or not usuario["ativo"]:
        connection.close()
        return jsonify({"erro":"Aluno não encontrado ou inativo"}),404

    material=connection.execute("SELECT id,nome,quantidade,ativo FROM materiais WHERE id=?",(material_id,)).fetchone()
    if not material or not material["ativo"]:
        connection.close()
        return jsonify({"erro":"Material não encontrado ou inativo"}),404
    if material["quantidade"]<=0:
        connection.close()
        return jsonify({"erro":"Material sem estoque"}),409

    if maquina_id:
        maquina=connection.execute("SELECT id FROM maquinas WHERE id=?",(maquina_id,)).fetchone()
        if not maquina:
            connection.close()
            return jsonify({"erro":"Máquina não encontrada"}),404

    token=None
    for _ in range(20):
        candidato=gerar_token()
        if not connection.execute("SELECT id FROM tokens WHERE token=?",(candidato,)).fetchone():
            token=candidato
            break
    if token is None:
        connection.close()
        return jsonify({"erro":"Não foi possível gerar um token único"}),500

    criado_em=agora_utc().isoformat()
    expira_em=criar_validade().isoformat()
    connection.execute("""INSERT INTO tokens
        (token,usuario_id,material_id,maquina_id,criado_em,expira_em,status)
        VALUES (?,?,?,?,?,?,'disponivel')""",
        (token,usuario_id,material_id,maquina_id,criado_em,expira_em))
    connection.commit()
    connection.close()

    return jsonify({
        "sucesso":True,"token":token,"material":material["nome"],
        "material_id":material_id,"aluno_id":usuario_id,
        "maquina_id":maquina_id,"criado_em":criado_em,"validade":expira_em
    }),201
