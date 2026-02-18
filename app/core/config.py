from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    HOST: str
    PORT: int

    # JWT
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Mongo
    MONGO_HOST_URL: str
    MONGO_DATABASE: str = "suggestions"
    MONGO_USER_COLLECTION: str = "users"
    MONGO_SONGS_COLLECTION: str = "songs"
    MONGO_HISTORY_COLLECTION: str = "history"

    # Qdrant
    QDRANT_URL: str
    QDRANT_SONGS_COLLECTION: str = "songs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
