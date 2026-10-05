from datetime import datetime, timezone

def agora_iso():
    return datetime.now(timezone.utc).isoformat()
