from flask import Blueprint, jsonify
from app.database.database import get_db
from app.services.token_service import token_expirado

tokens_bp = Blueprint("tokens", __name__)


def atualizar_expirados(connection):
    registros = connection.execute(
        "SELECT id, expira_em FROM tokens WHERE status='disponivel'"
    ).fetchall()

    for registro in registros:
        if token_expirado(registro["expira_em"]):
            connection.execute(
                "UPDATE tokens SET status='expirado' WHERE id=?",
                (registro["id"],)
            )

    connection.commit()


@tokens_bp.get("/tokens")
def listar_tokens():
    connection = get_db()
    atualizar_expirados(connection)

    registros = connection.execute(
        """
        SELECT
            t.id,
            t.token,
            t.usuario_id,
            u.nome AS aluno,
            t.material_id,
            m.nome AS material,
            t.maquina_id,
            ma.codigo AS maquina,
            t.criado_em,
            t.expira_em,
            t.status
        FROM tokens t
        JOIN usuarios u ON u.id = t.usuario_id
        JOIN materiais m ON m.id = t.material_id
        LEFT JOIN maquinas ma ON ma.id = t.maquina_id
        ORDER BY t.id DESC
        """
    ).fetchall()

    connection.close()
    return jsonify([dict(registro) for registro in registros])


@tokens_bp.get("/tokens/<token>")
def consultar_token(token):
    connection = get_db()

    registro = connection.execute(
        """
        SELECT
            t.id,
            t.token,
            t.usuario_id,
            t.material_id,
            t.maquina_id,
            t.criado_em,
            t.expira_em,
            t.status,
            m.nome AS material
        FROM tokens t
        JOIN materiais m ON m.id = t.material_id
        WHERE t.token=?
        """,
        (token,)
    ).fetchone()

    if not registro:
        connection.close()
        return jsonify({"erro": "Token não encontrado"}), 404

    status = registro["status"]

    if status == "disponivel" and token_expirado(registro["expira_em"]):
        connection.execute(
            "UPDATE tokens SET status='expirado' WHERE id=?",
            (registro["id"],)
        )
        connection.commit()
        status = "expirado"

    connection.close()

    return jsonify({
        "token": registro["token"],
        "status": status,
        "aluno_id": registro["usuario_id"],
        "material_id": registro["material_id"],
        "material": registro["material"],
        "maquina_id": registro["maquina_id"],
        "criado_em": registro["criado_em"],
        "expira_em": registro["expira_em"]
    })
