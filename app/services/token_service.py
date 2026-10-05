import secrets
from datetime import datetime, timedelta, timezone
from flask import current_app

def agora_utc():
    return datetime.now(timezone.utc)

def gerar_token():
    return str(secrets.randbelow(900000) + 100000)

def criar_validade():
    return agora_utc() + timedelta(minutes=current_app.config["TOKEN_EXPIRATION_MINUTES"])

def token_expirado(expira_em):
    data=datetime.fromisoformat(expira_em)
    if data.tzinfo is None:
        data=data.replace(tzinfo=timezone.utc)
    return agora_utc() >= data
