from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    database_path: str = os.getenv("DATABASE_PATH")
    secret_key: str = os.getenv("SECRET_KEY")
    alghoritm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    
    class Config:
        env_file = ".env"

settings = Settings()