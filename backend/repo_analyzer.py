from __future__ import annotations

import re
import zipfile
from io import BytesIO
from pathlib import PurePosixPath
from typing import Optional

from component_extractor import (
    DISPLAY_NAMES,
    KNOWN_BACKBONES,
    KNOWN_DATASETS,
    KNOWN_LOSSES,
    KNOWN_METRICS,
    KNOWN_MODELS,
    KNOWN_OPTIMIZERS,
)

IGNORE_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "env", "dist", "build"}

EXACT_RELEVANT_NAMES = {
    "readme.md",
    "requirements.txt",
    "pyproject.toml",
    "environment.yml",
    "train.py",
    "eval.py",
    "test.py",
}
CONFIG_EXTENSIONS = {".yaml", ".yml", ".json", ".cfg", ".ini", ".toml"}

MAX_READ_BYTES = 200_000  # cap per-file read size for hint extraction
MAX_FILES_READ = 50  # cap number of files whose contents are read

EMPTY_CODE_HINTS = {
    "models": [],
    "backbones": [],
    "losses": [],
    "optimizers": [],
    "datasets": [],
    "metrics": [],
    "config": {},
}

GITHUB_URL_RE = re.compile(
    r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)

CLASS_MODEL_RE = re.compile(r"class\s+(\w+)\s*\(\s*(?:nn\.Module|torch\.nn\.Module)\s*\)")
CLASS_LOSS_RE = re.compile(r"class\s+(\w+(?:[Ll]oss))\s*\(")
OPTIMIZER_CALL_RE = re.compile(r"(?:optim|torch\.optim)\.(\w+)\s*\(")
CONFIG_LR_RE = re.compile(r"(?:learning[_ ]rate|lr)\s*[=:]\s*([0-9]+\.?[0-9]*(?:e-?[0-9]+)?)", re.IGNORECASE)
CONFIG_BATCH_RE = re.compile(r"batch[_ ]size\s*[=:]\s*([0-9]+)", re.IGNORECASE)
CONFIG_EPOCH_RE = re.compile(r"(?:num[_ ]epochs|epochs)\s*[=:]\s*([0-9]+)", re.IGNORECASE)


def _display(term: str) -> str:
    return DISPLAY_NAMES.get(term, term.title())


def is_safe_member(name: str) -> bool:
    if name.startswith("/") or name.startswith("\\"):
        return False
    if ".." in PurePosixPath(name).parts:
        return False
    return True


def is_ignored(name: str) -> bool:
    return any(part in IGNORE_DIRS for part in PurePosixPath(name).parts)


def is_relevant_file(name: str) -> bool:
    path = PurePosixPath(name)
    stem = path.stem.lower()
    suffix = path.suffix.lower()
    base = path.name.lower()
    if base in EXACT_RELEVANT_NAMES:
        return True
    if "model" in stem:
        return True
    if "loss" in stem:
        return True
    if "dataset" in stem or stem in {"data", "datasets"}:
        return True
    if "config" in stem or suffix in CONFIG_EXTENSIONS:
        return True
    return False


def parse_github_url(url: str) -> Optional[dict]:
    match = GITHUB_URL_RE.match(url.strip())
    if not match:
        return None
    return {"owner": match.group(1), "repo": match.group(2)}


def analyze_zip(content: bytes) -> dict:
    """Read a ZIP in-memory (no extraction to disk) and collect relevant files/contents."""
    try:
        zf = zipfile.ZipFile(BytesIO(content))
    except zipfile.BadZipFile as exc:
        return {"error": f"Could not read ZIP: {exc}", "repo_name": None, "relevant_files": [], "contents": {}}

    relevant_files: list[str] = []
    contents: dict[str, str] = {}
    top_level_roots: set[str] = set()

    for info in zf.infolist():
        name = info.filename
        if not is_safe_member(name) or is_ignored(name):
            continue
        parts = PurePosixPath(name).parts
        if parts:
            top_level_roots.add(parts[0])

    # A "repo name" only makes sense if every entry shares one common top-level folder
    repo_name = next(iter(top_level_roots)) if len(top_level_roots) == 1 else None

    for info in zf.infolist():
        name = info.filename
        if info.is_dir() or not is_safe_member(name) or is_ignored(name):
            continue

        if not is_relevant_file(name):
            continue

        relevant_files.append(name)
        if len(contents) < MAX_FILES_READ:
            try:
                raw = zf.read(info)[:MAX_READ_BYTES]
                contents[name] = raw.decode("utf-8", errors="ignore")
            except Exception:
                pass

    return {
        "error": None,
        "repo_name": repo_name,
        "relevant_files": sorted(relevant_files),
        "contents": contents,
    }


def extract_code_hints(contents: dict) -> dict:
    combined = "\n".join(contents.values())
    lowered = combined.lower()

    models = {_display(t) for t in KNOWN_MODELS if t in lowered}
    models |= {
        m.group(1) for m in CLASS_MODEL_RE.finditer(combined) if "loss" not in m.group(1).lower()
    }

    backbones = {_display(t) for t in KNOWN_BACKBONES if t in lowered}

    losses = {_display(t) for t in KNOWN_LOSSES if t in lowered}
    losses |= {m.group(1) for m in CLASS_LOSS_RE.finditer(combined)}

    optimizers = {_display(t) for t in KNOWN_OPTIMIZERS if t in lowered}
    optimizers |= {m.group(1) for m in OPTIMIZER_CALL_RE.finditer(combined)}

    datasets = {_display(t) for t in KNOWN_DATASETS if t in lowered}
    metrics = {_display(t) for t in KNOWN_METRICS if t in lowered}

    config: dict[str, str] = {}
    lr = CONFIG_LR_RE.search(combined)
    bs = CONFIG_BATCH_RE.search(combined)
    ep = CONFIG_EPOCH_RE.search(combined)
    if lr:
        config["learningRate"] = lr.group(1)
    if bs:
        config["batchSize"] = bs.group(1)
    if ep:
        config["epochs"] = ep.group(1)

    return {
        "models": sorted(models),
        "backbones": sorted(backbones),
        "losses": sorted(losses),
        "optimizers": sorted(optimizers),
        "datasets": sorted(datasets),
        "metrics": sorted(metrics),
        "config": config,
    }


def analyze_repo(github_url: Optional[str], zip_content: Optional[bytes]) -> dict:
    """Build a dict matching the RepoAnalysis schema from an optional GitHub URL or ZIP upload."""
    if zip_content:
        result = analyze_zip(zip_content)
        if result["error"]:
            return {
                "inputType": "zip",
                "repoName": None,
                "status": result["error"],
                "relevantFiles": [],
                "fileCount": 0,
                "codeHints": EMPTY_CODE_HINTS,
            }
        return {
            "inputType": "zip",
            "repoName": result["repo_name"],
            "status": "ZIP analyzed successfully",
            "relevantFiles": result["relevant_files"],
            "fileCount": len(result["relevant_files"]),
            "codeHints": extract_code_hints(result["contents"]),
        }

    if github_url:
        parsed = parse_github_url(github_url)
        if not parsed:
            return {
                "inputType": "github",
                "repoName": None,
                "status": "Invalid GitHub URL",
                "relevantFiles": [],
                "fileCount": 0,
                "codeHints": EMPTY_CODE_HINTS,
            }
        return {
            "inputType": "github",
            "repoName": f"{parsed['owner']}/{parsed['repo']}",
            "status": "GitHub URL received, cloning not implemented yet",
            "relevantFiles": [],
            "fileCount": 0,
            "codeHints": EMPTY_CODE_HINTS,
        }

    return {
        "inputType": "none",
        "repoName": None,
        "status": "No repository or code provided",
        "relevantFiles": [],
        "fileCount": 0,
        "codeHints": EMPTY_CODE_HINTS,
    }
