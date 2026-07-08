from __future__ import annotations

import re
from typing import Optional

SECTION_DISPLAY = {
    "abstract": "Abstract",
    "introduction": "Introduction",
    "related_work": "Related Work",
    "method": "Method",
    "implementation_details": "Implementation Details",
    "experiments": "Experiments",
    "results": "Results",
    "conclusion": "Conclusion",
}

CATEGORY_LABELS = {
    "model": "Method / Architecture",
    "loss": "Training Objective / Loss",
    "optimizer": "Experiment / Training Setup",
    "metrics": "Evaluation / Results",
    "dataset": "Dataset / Experiments",
}

SECTION_PRIORITY = {
    "model": ["method", "introduction", "abstract"],
    "loss": ["method", "experiments"],
    "optimizer": ["experiments", "implementation_details", "method"],
    "metrics": ["results", "experiments"],
    "dataset": ["experiments", "implementation_details", "results", "method"],
}

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _matched_sentence(body: str, term: str) -> Optional[str]:
    """First sentence in *body* containing *term* (case-insensitive), trimmed for display."""
    if not body or not term:
        return None
    lowered_term = term.lower()
    for sentence in _SENTENCE_SPLIT_RE.split(body):
        if lowered_term in sentence.lower():
            return sentence.strip()[:240]
    return None

FILE_KEYWORDS = {
    "model": ["model"],
    "loss": ["loss"],
    "optimizer": ["train", "config", "optim"],
    "metrics": ["eval", "test", "metric"],
    "dataset": ["dataset", "data"],
}

REFERENCE_PREVIEW_CHARS = 120
MAX_MAPPINGS = 10
_CONFIDENCE_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def _find_file(relevant_files: list[str], keywords: list[str]) -> Optional[str]:
    for f in relevant_files:
        name = f.lower()
        if any(k in name for k in keywords):
            return f
    return None


def _reference_preview(body: str, header: str) -> str:
    preview = body[:REFERENCE_PREVIEW_CHARS].strip()
    if len(body) > REFERENCE_PREVIEW_CHARS:
        preview = preview.rstrip() + "…"
    return preview or header


def _find_term_section(term: str, sections: dict, priority: list[str]) -> tuple[Optional[str], Optional[str], str]:
    """
    Returns (section_key, reference_snippet, section_body) for *term* specifically — prefers
    the first priority section whose body actually mentions the term (so the evidence sentence
    is real), falling back to the first existing priority section otherwise (weaker evidence:
    the section is plausible by priority but doesn't literally contain the term).
    """
    fallback: Optional[tuple[str, str, str]] = None
    for key in priority:
        if key not in sections:
            continue
        body = sections[key].get("body", "")
        header = sections[key].get("header", SECTION_DISPLAY.get(key, key))
        if fallback is None:
            fallback = (key, _reference_preview(body, header), body)
        if term.lower() in body.lower():
            return key, _reference_preview(body, header), body
    return fallback if fallback else (None, None, "")


def _confidence(has_file: bool, has_section: bool) -> str:
    if has_file and has_section:
        return "High"
    if has_file or has_section:
        return "Medium"
    return "Low"


def _build_category(category: str, terms: list[str], sections: dict, relevant_files: list[str], explain: str) -> list[dict]:
    if not terms:
        return []

    file_match = _find_file(relevant_files, FILE_KEYWORDS[category])

    items = []
    for term in terms:
        section_key, reference, body = _find_term_section(term, sections, SECTION_PRIORITY[category])
        section_label = SECTION_DISPLAY.get(section_key, CATEGORY_LABELS[category]) if section_key else CATEGORY_LABELS[category]
        confidence = _confidence(file_match is not None, section_key is not None)
        code_block = f"{file_match} > {term}" if file_match else term
        if section_key:
            explanation = f"{explain.format(term=term)} (found in the {section_label} section)."
        else:
            explanation = f"{explain.format(term=term)}, but no matching section was clearly identified in the paper."
        items.append(
            {
                "codeBlock": code_block,
                "paperSection": section_label,
                "paperReference": reference or "Not found in paper",
                "explanation": explanation,
                "confidence": confidence,
                "evidenceSentence": _matched_sentence(body, term) if section_key else None,
            }
        )
    return items


def build_mappings(sections: dict, code_hints: dict, relevant_files: list[str]) -> list[dict]:
    """
    Map repository code evidence to specific paper sections.
    sections: paper section dict from parse_pdf(), e.g. {"method": {"header": ..., "body": ...}}
    code_hints: extracted CodeHints dict (models/backbones/losses/optimizers/datasets/metrics/config)
    relevant_files: list of relevant repo file paths
    """
    model_terms = list(dict.fromkeys(code_hints["models"] + code_hints["backbones"]))

    mappings: list[dict] = []
    mappings += _build_category(
        "model", model_terms, sections, relevant_files,
        "{term} appears to implement the model architecture described in the paper",
    )
    mappings += _build_category(
        "loss", code_hints["losses"], sections, relevant_files,
        "{term} appears to implement the training objective described in the paper",
    )
    mappings += _build_category(
        "optimizer", code_hints["optimizers"], sections, relevant_files,
        "{term} matches the optimizer configuration described in the paper",
    )
    mappings += _build_category(
        "metrics", code_hints["metrics"], sections, relevant_files,
        "{term} matches an evaluation metric reported in the paper",
    )
    mappings += _build_category(
        "dataset", code_hints["datasets"], sections, relevant_files,
        "{term} matches the dataset referenced in the paper",
    )

    mappings.sort(key=lambda m: _CONFIDENCE_ORDER[m["confidence"]])
    return mappings[:MAX_MAPPINGS]
