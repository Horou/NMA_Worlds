from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_TYPE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_URL: str

    ROOT_PATH: str
    FILES_PATH: str


settings = Settings()
