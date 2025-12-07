"""
Application configuration
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TOKEN: str = "changeme"
    
    # YandexGPT Settings
    YANDEX_API_KEY: str = ""
    YANDEX_FOLDER_ID: str = ""
    YANDEX_MODEL: str = "yandexgpt-lite"
    
    # Qdrant Settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "course_materials"
    
    # PostgreSQL Settings
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "rag_service"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    
    # Embeddings Settings
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # Performance Settings
    MAX_CHUNKS: int = 5
    MAX_CONTEXT_LENGTH: int = 3000
    REQUEST_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()

