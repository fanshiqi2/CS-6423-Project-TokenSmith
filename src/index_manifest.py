from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


def compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def manifest_path(artifacts_dir: Path, index_prefix: str) -> Path:
    return artifacts_dir / f"{index_prefix}_manifest.json"


def load_manifest(artifacts_dir: Path, index_prefix: str) -> Dict[str, Any]:
    path = manifest_path(artifacts_dir, index_prefix)
    if not path.exists():
        return {
            "version": 1,
            "index_prefix": index_prefix,
            "documents": {}
        }
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: Dict[str, Any], artifacts_dir: Path, index_prefix: str) -> None:
    path = manifest_path(artifacts_dir, index_prefix)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def build_doc_record(path: Path, sha256: str, chunk_start: int, chunk_end: int) -> Dict[str, Any]:
    chunk_count = 0 if chunk_end < chunk_start else (chunk_end - chunk_start + 1)
    return {
        "path": str(path),
        "sha256": sha256,
        "chunk_start": chunk_start,
        "chunk_end": chunk_end,
        "chunk_count": chunk_count,
        "indexed_at": datetime.now(timezone.utc).isoformat()
    }