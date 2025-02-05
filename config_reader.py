from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    bot_token: SecretStr
    weather_api_key: str
    nutritionix_app_id: str
    nutritionix_api_key: str

    class Config:
        env_file = ".env"
        extra = "ignore"

config = Config()