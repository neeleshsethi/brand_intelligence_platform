from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API Config
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"

    # Mock Mode (for demos without LLM calls)
    MOCK_MODE: bool = False

    # Demo Mode (uses cached responses for impressive speed)
    DEMO_MODE: bool = False

    # OpenAI
    OPENAI_API_KEY: str = ""

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "pfizer-brand-planning"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # Retry configuration
    MAX_RETRIES: int = 3
    RETRY_WAIT_SECONDS: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
