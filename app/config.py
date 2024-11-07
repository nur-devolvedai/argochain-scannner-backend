# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    mongo_uri = os.getenv("MONGO_URI")
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm = os.getenv("JWT_ALGORITHM")
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
