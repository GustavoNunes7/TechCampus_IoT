from flask import Blueprint, jsonify
from app.database.database import get_db

health_bp=Blueprint("health",__name__)

@health_bp.get("/health")
def health():
    connection=get_db()
    connection.execute("SELECT 1")
    connection.close()
    return jsonify({"status":"online","servico":"TechCampus IoT"})
