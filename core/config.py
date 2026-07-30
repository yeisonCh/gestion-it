from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    # Base de datos
    DB_SERVER: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Aplicación
    APP_NAME: str = "Sistema Mantenimiento PC"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
    env_file=".env",
    case_sensitive=True
    )

    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_SERVER}/{self.DB_NAME}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )



settings = Settings()