from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "JobMatch MVP API"
    mongo_uri: str = "mongodb://mongo:27017"
    mongo_db: str = "jobmatch"
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    admin_password: str = "admin123"
    admin_token_secret: str = "change-me"
    embed_use_sentence_transformers: bool = False
    embedding_dim: int = 384
    match_top_k: int = 10

    class Config:
        env_file = ".env"
        env_prefix = ""


settings = Settings()
