import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "techcampus_iot.db")
    IOT_API_KEY = os.getenv("IOT_API_KEY", "dev-iot-key")
    TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES", "10"))
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
