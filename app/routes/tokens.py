from flask import Blueprint, jsonify, Response
from app.database.database import get_db
from app.services.token_service import token_expirado

tokens_bp = Blueprint("tokens", __name__)

@tokens_bp.get("/tokens")
def listar_tokens():
    connection = get_db()
    registros_ativos = connection.execute(
        "SELECT id, expira_em FROM tokens WHERE status='disponivel'"
    ).fetchall()
    for registro in registros_ativos:
        if token_expirado(registro["expira_em"]):
            connection.execute("UPDATE tokens SET status='expirado' WHERE id=?", (registro["id"],))
    connection.commit()
    registros = connection.execute("""
        SELECT t.id,t.token,t.usuario_id,u.nome AS aluno,t.material_id,m.nome AS material,
               t.maquina_id,ma.codigo AS maquina,t.criado_em,t.expira_em,t.status
        FROM tokens t
        JOIN usuarios u ON u.id=t.usuario_id
        JOIN materiais m ON m.id=t.material_id
        LEFT JOIN maquinas ma ON ma.id=t.maquina_id
        ORDER BY t.id DESC
    """).fetchall()
    connection.close()
    return jsonify([dict(registro) for registro in registros])

@tokens_bp.get("/tokens/<token>")
def consultar_token(token):
    connection = get_db()
    registro = connection.execute("""
        SELECT t.id,t.token,t.usuario_id,t.material_id,t.maquina_id,t.criado_em,t.expira_em,
               t.status,m.nome AS material
        FROM tokens t JOIN materiais m ON m.id=t.material_id WHERE t.token=?
    """,(token,)).fetchone()
    if not registro:
        connection.close()
        return jsonify({"erro":"Token não encontrado"}),404
    status=registro["status"]
    if status=="disponivel" and token_expirado(registro["expira_em"]):
        connection.execute("UPDATE tokens SET status='expirado' WHERE id=?",(registro["id"],))
        connection.commit()
        status="expirado"
    connection.close()
    return jsonify({"token":registro["token"],"status":status,"aluno_id":registro["usuario_id"],
                    "material_id":registro["material_id"],"material":registro["material"],
                    "maquina_id":registro["maquina_id"],"criado_em":registro["criado_em"],
                    "expira_em":registro["expira_em"]})

@tokens_bp.get("/tokens-painel")
def tokens_painel():
    return Response("<!DOCTYPE html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<title>Tokens • TechCampus IoT</title>\n<style>\n*{box-sizing:border-box}\nbody{margin:0;min-height:100vh;font-family:Arial,sans-serif;background:#080b10;color:#f5f7fa;padding:24px}\n.container{width:100%;max-width:1100px;margin:auto;background:#101722;border:1px solid #1d2a3a;border-radius:18px;padding:32px;box-shadow:0 20px 60px rgba(0,0,0,.35)}\n.header{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}\nh1{margin:0 0 8px}.subtitle{color:#aeb9c8;margin-top:0}\n.back{color:#9ec5f8;text-decoration:none}.back:hover{text-decoration:underline}\ntable{width:100%;border-collapse:collapse;margin-top:24px}\nth,td{text-align:left;padding:14px 10px;border-bottom:1px solid #26364a}\nth{color:#8fa2ba;font-size:13px;text-transform:uppercase}\n.status{display:inline-block;padding:6px 10px;border-radius:999px;background:#182334}\n.empty{text-align:center;color:#718096;padding:40px}\n.token{font-family:monospace;font-size:16px}\n@media(max-width:800px){table{display:block;overflow-x:auto;white-space:nowrap}}\n</style>\n</head>\n<body>\n<main class=\"container\">\n<div class=\"header\">\n<div><h1>Tokens</h1><p class=\"subtitle\">Tokens gerados pelo servidor TechCampus IoT.</p></div>\n<a class=\"back\" href=\"/\">← Voltar ao início</a>\n</div>\n<table>\n<thead><tr><th>Token</th><th>Aluno</th><th>Material</th><th>Máquina</th><th>Validade</th><th>Status</th></tr></thead>\n<tbody id=\"tokens\"><tr><td colspan=\"6\" class=\"empty\">Carregando...</td></tr></tbody>\n</table>\n</main>\n<script>\nasync function carregarTokens(){\n const corpo=document.getElementById(\"tokens\");\n try{\n   const resposta=await fetch(\"/api/tokens\");\n   const dados=await resposta.json();\n   if(!dados.length){corpo.innerHTML='<tr><td colspan=\"6\" class=\"empty\">Nenhum token foi gerado ainda.</td></tr>';return;}\n   corpo.innerHTML=dados.map(t=>'<tr>'+\n     '<td class=\"token\">'+t.token+'</td>'+\n     '<td>'+t.aluno+'</td>'+\n     '<td>'+t.material+'</td>'+\n     '<td>'+(t.maquina||\"Não definida\")+'</td>'+\n     '<td>'+new Date(t.expira_em).toLocaleString(\"pt-BR\")+'</td>'+\n     '<td><span class=\"status\">'+t.status+'</span></td>'+\n   '</tr>').join(\"\");\n }catch(e){corpo.innerHTML='<tr><td colspan=\"6\" class=\"empty\">Não foi possível carregar os tokens.</td></tr>';}\n}\ncarregarTokens();\nsetInterval(carregarTokens,5000);\n</script>\n</body>\n</html>", mimetype="text/html")
