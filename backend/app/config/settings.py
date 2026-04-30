"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration for the AI Insights Assistant backend.

    Values are read from environment variables or a .env file.
    """

    # --- Application ---
    app_name: str = "AI Insights Assistant"
    debug: bool = False

    # --- Database ---
    database_path: str = "data/app.db"

    # --- JWT Authentication ---
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # --- AI Model Provider ---
    model_provider: str = "gemini"
    model_name: str = "gemini-2.5-flash"
    openai_api_key: str = ""  # Also used for Gemini API key
    gemini_api_key: str = ""
    openai_base_url: str = ""  # Custom base URL for OpenAI-compatible APIs

    # --- Tool Configuration ---
    sql_row_limit: int = 500
    csv_row_limit: int = 500
    pdf_top_k: int = 5
    pdf_relevance_threshold: float = 0.3
    pdf_chunk_size: int = 1000
    pdf_chunk_overlap: int = 200

    # --- Data Paths ---
    data_dir: str = "data"
    pdf_storage_dir: str = "data/pdfs"
    csv_storage_dir: str = "data/csvs"

    # --- ChromaDB ---
    chroma_persist_dir: str = "data/chroma"

    # --- Input Validation ---
    max_question_length: int = 2000

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
