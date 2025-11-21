"""Application settings and environment-driven configuration.

Placeholders only — do NOT commit real keys. Use `.env` for secrets.
This module avoids a pydantic BaseSettings dependency to keep runtime
simple for the demo environment. Replace with pydantic-settings in
production if desired.
"""
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()


@dataclass
class Settings:
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "./.vector_store")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_MODE: str = os.getenv("APP_MODE", "demo")

    # Decision weights for fusion scoring
    WEIGHT_AFFORDABILITY: float = float(os.getenv("WEIGHT_AFFORDABILITY", 0.25))
    WEIGHT_PRICE: float = float(os.getenv("WEIGHT_PRICE", 0.25))
    WEIGHT_SENTIMENT: float = float(os.getenv("WEIGHT_SENTIMENT", 0.2))
    WEIGHT_AVAILABILITY: float = float(os.getenv("WEIGHT_AVAILABILITY", 0.15))
    WEIGHT_PREFERENCE: float = float(os.getenv("WEIGHT_PREFERENCE", 0.15))

    BUY_THRESHOLD: float = float(os.getenv("BUY_THRESHOLD", 0.6))


settings = Settings()
