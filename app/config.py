"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    groq_api_key: str | None
    groq_model: str
    parcle_api_key: str | None
    parcle_user_id: str
    enterpro_url: str | None
    enterpro_api_key: str | None
    enterpro_command: str | None
    enterpro_workspace_id: str | None
    employee_portal_path: Path
    parcle_memory_dir: str
    external_request_timeout: float
    validation_command: str
    require_clean_target_repo: bool
    enable_git_push: bool
    github_token: str | None
    github_base_branch: str
    github_api_url: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            parcle_api_key=os.getenv("PARCLE_API_KEY"),
            parcle_user_id=os.getenv("PARCLE_USER_ID", "system_user"),
            enterpro_url=os.getenv("ENTERPRO_URL") or os.getenv("ENTER_PRO_URL"),
            enterpro_api_key=os.getenv("ENTERPRO_API_KEY"),
            enterpro_command=os.getenv("ENTERPRO_COMMAND"),
            enterpro_workspace_id=os.getenv("ENTERPRO_WORKSPACE_ID"),
            employee_portal_path=Path(os.getenv("EMPLOYEE_PORTAL_PATH", ".")).resolve(),
            parcle_memory_dir=os.getenv("PARCLE_MEMORY_DIR", "docs/parcle_memory"),
            external_request_timeout=float(os.getenv("EXTERNAL_REQUEST_TIMEOUT", "60")),
            validation_command=os.getenv("VALIDATION_COMMAND", "pytest -q"),
            require_clean_target_repo=_as_bool(os.getenv("REQUIRE_CLEAN_TARGET_REPO"), default=False),
            enable_git_push=_as_bool(os.getenv("ENABLE_GIT_PUSH"), default=False),
            github_token=os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"),
            github_base_branch=os.getenv("GITHUB_BASE_BRANCH", "main"),
            github_api_url=os.getenv("GITHUB_API_URL", "https://api.github.com"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


settings = Settings.from_env()
