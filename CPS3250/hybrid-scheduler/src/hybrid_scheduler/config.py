from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


def _read_local_env(path: Path = ENV_FILE) -> dict[str, str]:
    """Read the small KEY=VALUE subset used by this project.

    Real process environment variables take precedence later. Values are never
    expanded or executed, which keeps this loader predictable and dependency
    free. Secret managers or container environment injection remain preferable
    for non-local deployments.
    """

    if not path.is_file():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value[:1] == value[-1:] and value[:1] in {'"', "'"}:
            value = value[1:-1]
        if key:
            values[key] = value

    return values


class Settings(BaseModel):
    """Central configuration with secrets redacted from repr/serialization."""

    app_name: str = "Hybrid Scheduler"
    environment: str = "dev"
    host: str = "127.0.0.1"
    port: int = Field(8080, ge=1, le=65535)
    api_key: SecretStr | None = None
    rabbitmq_url: SecretStr | None = None
    aws_region: str = "us-east-1"
    prom_port: int = Field(8000, ge=1, le=65535)


def _optional_secret(value: str | None) -> SecretStr | None:
    return SecretStr(value) if value else None


@lru_cache()
def get_settings() -> Settings:
    """Load .env once, with real environment variables taking precedence."""

    local = _read_local_env()

    def value(name: str, default: str) -> str:
        return os.environ.get(name, local.get(name, default))

    return Settings(
        app_name=value("APP_NAME", "Hybrid Scheduler"),
        environment=value("ENVIRONMENT", "dev"),
        host=value("HOST", "127.0.0.1"),
        port=int(value("PORT", "8080")),
        api_key=_optional_secret(value("API_KEY", "")),
        rabbitmq_url=_optional_secret(value("RABBITMQ_URL", "")),
        aws_region=value("AWS_REGION", "us-east-1"),
        prom_port=int(value("PROM_PORT", "8000")),
    )
