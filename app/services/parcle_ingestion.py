from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.integrations.parcle import ParcleClient

EMPLOYEE_PORTAL_MEMORY_FILES = (
    "API_DOCUMENTATION.md",
    "PARCLE_MEMORY.md",
    "README.md",
)


class ParcleIngestionService:
    def __init__(self, client: ParcleClient, project_path: Path, memory_dir: str = "docs/parcle_memory"):
        self.client = client
        self.project_path = project_path.resolve()
        self.memory_path = (self.project_path / memory_dir).resolve()

    def load_documents(self) -> list[dict[str, Any]]:
        if self.memory_path.is_dir():
            files = sorted(self.memory_path.rglob("*.md"))
            if not files:
                raise FileNotFoundError(f"No Markdown files found in Parcle memory folder: {self.memory_path}")
        else:
            missing = [name for name in EMPLOYEE_PORTAL_MEMORY_FILES if not (self.project_path / name).is_file()]
            if missing:
                raise FileNotFoundError(
                    f"Missing Parcle memory folder {self.memory_path} and required fallback files in "
                    f"{self.project_path}: {', '.join(missing)}"
                )
            files = [self.project_path / name for name in EMPLOYEE_PORTAL_MEMORY_FILES]

        documents: list[dict[str, Any]] = []
        for path in files:
            reference = path.relative_to(self.project_path).as_posix()
            content = path.read_text(encoding="utf-8")
            checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()
            documents.append(
                {
                    "path": path,
                    "reference": reference,
                    "metadata": {
                        "repository": "employee-portal",
                        "source_path": reference,
                        "content_type": "project_documentation",
                        "sha256": checksum,
                        "indexed_at": datetime.now(timezone.utc).isoformat(),
                    },
                }
            )
        return documents

    def ingest(self, dry_run: bool = False) -> dict[str, Any]:
        documents = self.load_documents()
        checksums = {
            document["reference"]: document["metadata"]["sha256"] for document in documents
        }
        if dry_run:
            return {
                "dry_run": True,
                "location": self.client.memory_location,
                "documents_submitted": 0,
                "documents_found": [document["reference"] for document in documents],
                "checksums": checksums,
            }

        result = self.client.ingest_files([document["path"] for document in documents])
        result["documents_found"] = [document["reference"] for document in documents]
        result["checksums"] = checksums
        return result
