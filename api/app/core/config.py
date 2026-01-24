from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "JobMatch MVP API"
    mongodb_uri: str = Field(default="mongodb://mongo:27017", alias="MONGODB_URI")
    mongo_db: str = Field(default="jobmatch", alias="MONGO_DB")
    qdrant_url: str = Field(default="http://qdrant:6333", alias="QDRANT_URL")
    admin_password: str = Field(default="admin123", alias="ADMIN_PASSWORD")
    admin_token_secret: str = Field(default="change-me", alias="ADMIN_TOKEN_SECRET")
    embed_use_sentence_transformers: bool = Field(default=False, alias="EMBED_USE_SENTENCE_TRANSFORMERS")
    embedding_dim: int = Field(default=384, alias="EMBEDDING_DIM")
    match_top_k: int = Field(default=10, alias="MATCH_TOP_K")

    class Config:
        env_file = ".env"
        env_prefix = ""
        populate_by_name = True


settings = Settings()
