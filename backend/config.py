# backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file (only in dev)
load_dotenv()

class Settings:
    def __init__(self):
        self.DATABASE_URL = self.require("DATABASE_URL")
        self.SECRET_KEY = self.require("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
        self.ENV = os.getenv("ENV", "development")

    def require(self, var_name):
        value = os.getenv(var_name)
        if value is None or value.strip() == "":
            raise ValueError(f"❌ Required environment variable '{var_name}' is missing or empty.")
        return value

# Singleton instance
settings = Settings()
