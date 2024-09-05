from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensetive = False,
    )
    BOT_TOKEN: str

settings = Settings()
DATABASE_URI = 'postgresql://postgres:1202@localhost/bot'

if __name__ == "__main__":
    print(settings.BOT_TOKEN)