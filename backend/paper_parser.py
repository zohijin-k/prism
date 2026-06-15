from __future__ import annotations

import re
from io import BytesIO
from typing import Optional

from pypdf import PdfReader
from pypdf.errors import PdfReadError

PREVIEW_CHARS = 800
SECTION_PREVIEW_CHARS = 200

# Canonical section keys in reading order
SECTION_ORDER = [
    "abstract",
    "introduction",
    "related_work",
    "method",
    "experiments",
    "results",
    "conclusion",
]

# Aliases recognised as each section header (matched case-insensitively, exact line)
SECTION_ALIASES: dict[str, list[str]] = {
    "abstract": [
        "abstract",
    ],
    "introduction": [
        "introduction",
    ],
    "related_work": [
        "related work",
        "related works",
        "background",
        "prior work",
        "literature review",
        "related literature",
    ],
    "method": [
        "method",
        "methods",
        "methodology",
        "approach",
        "our approach",
        "proposed method",
        "proposed approach",
        "model",
        "model architecture",
        "architecture",
        "framework",
    ],
    "experiments": [
        "experiments",
        "experiment",
        "experimental setup",
        "experimental results",
        "experimental evaluation",
        "implementation",
        "implementation details",
        "setup",
    ],
    "results": [
        "results",
        "result",
        "evaluation",
        "performance",
        "quantitative results",
        "quantitative evaluation",
        "analysis",
    ],
    "conclusion": [
        "conclusion",
        "conclusions",
        "discussion",
        "summary",
        "concluding remarks",
        "future work",
    ],
}

# Pre-compiled strip pattern for numbering prefixes like "1.", "2.1", "III.", "A."
_NUM_PREFIX = re.compile(
    r"^\s*(?:\d+\.?[\d.]*|[IVX]+\.|[A-Z]\.)\s*",
    re.IGNORECASE,
)


def _match_section_key(line: str) -> str | None:
    """Return a section key if *line* is a known section header, else None."""
    if not line or len(line) > 100:
        return None
    clean = _NUM_PREFIX.sub("", line).strip().lower()
    # Remove trailing period
    clean = clean.rstrip(".")
    if not clean:
        return None
    for key, aliases in SECTION_ALIASES.items():
        if clean in aliases:
            return key
    return None


def _detect_sections(text: str) -> dict[str, dict[str, str]]:
    """
    Split *text* into labelled sections by scanning for known headers.
    Returns {section_key: {"header": str, "body": str}}.
    First occurrence of each key wins; later duplicates are appended to the body.
    """
    sections: dict[str, dict[str, str]] = {}
    current_key: str | None = None
    current_header = ""
    current_lines: list[str] = []

    for line in text.splitlines():
        key = _match_section_key(line.strip())
        if key:
            if key not in sections:
                # Flush previous section
                if current_key:
                    sections[current_key] = {
                        "header": current_header,
                        "body": "\n".join(current_lines).strip(),
                    }
                current_key = key
                current_header = line.strip()
                current_lines = []
            else:
                # Duplicate header — treat as body text of the current section
                if current_key:
                    current_lines.append(line)
        else:
            if current_key is not None:
                current_lines.append(line)

    # Flush last section
    if current_key:
        sections[current_key] = {
            "header": current_header,
            "body": "\n".join(current_lines).strip(),
        }

    return sections


def extract_paper_info(filename: str, content: bytes) -> dict:
    """
    Extract metadata, text preview, and section structure from a PDF.
    Returns a dict matching PaperInfo schema.
    Never raises — errors are captured in extraction_error.
    """
    try:
        reader = PdfReader(BytesIO(content))
        page_count = len(reader.pages)

        # Extract full text (needed for section detection)
        all_text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()

        if not all_text:
            return {
                "filename": filename,
                "page_count": page_count,
                "text_preview": "(No selectable text found — this PDF may be image-only or scanned.)",
                "extraction_error": None,
                "sections": {"detected": {}, "total_chars": 0},
            }

        # Build preview from the start of full text
        preview = all_text[:PREVIEW_CHARS]
        if len(all_text) > PREVIEW_CHARS:
            preview = preview.rstrip() + "…"

        # Detect sections
        raw = _detect_sections(all_text)
        detected: dict[str, dict] = {}
        for key, info in raw.items():
            body = info["body"]
            sec_preview = body[:SECTION_PREVIEW_CHARS]
            if len(body) > SECTION_PREVIEW_CHARS:
                sec_preview = sec_preview.rstrip() + "…"
            detected[key] = {
                "header": info["header"],
                "char_count": len(body),
                "preview": sec_preview,
            }

        return {
            "filename": filename,
            "page_count": page_count,
            "text_preview": preview,
            "extraction_error": None,
            "sections": {
                "detected": detected,
                "total_chars": sum(d["char_count"] for d in detected.values()),
            },
        }

    except PdfReadError as exc:
        return {
            "filename": filename,
            "page_count": 0,
            "text_preview": "",
            "extraction_error": f"Could not read PDF: {exc}",
            "sections": {"detected": {}, "total_chars": 0},
        }
    except Exception as exc:
        return {
            "filename": filename,
            "page_count": 0,
            "text_preview": "",
            "extraction_error": f"Unexpected error during extraction: {exc}",
            "sections": {"detected": {}, "total_chars": 0},
        }
