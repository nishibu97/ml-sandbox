import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    port: int = 8000
    log_level: str = "info"


def get_settings() -> Settings:
    return Settings(
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
    )
