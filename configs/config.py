from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensetive = False,
    )
    BOT_TOKEN: str

settings = Settings()
DATABASE_URI = 'postgresql://postgres:1202@postgres/bot'

if __name__ == "__main__":
    print(settings.BOT_TOKEN)