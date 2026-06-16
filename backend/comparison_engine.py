from __future__ import annotations

import re

STATUS_MATCH = "Match"
STATUS_PARTIAL = "Partial Match"
STATUS_MISMATCH = "Mismatch"
STATUS_PAPER_ONLY = "Paper Only"
STATUS_CODE_ONLY = "Code Only"
STATUS_UNKNOWN = "Unknown"

# Suffix words stripped during "core" comparison so e.g. "Cross Entropy" == "CrossEntropyLoss"
_CORE_SUFFIXES = ("loss", "function", "optimizer", "layer", "score", "coefficient")


def normalize(text: str) -> str:
    """Lowercase and collapse whitespace/hyphens/underscores: 'ResNet-50' -> 'resnet50'."""
    return re.sub(r"[\s\-_]+", "", text.lower().strip())


def normalize_core(text: str) -> str:
    """normalize() plus stripping a trailing descriptor word: 'CrossEntropyLoss' -> 'crossentropy'."""
    norm = normalize(text)
    for suffix in _CORE_SUFFIXES:
        if norm.endswith(suffix) and len(norm) > len(suffix):
            return norm[: -len(suffix)]
    return norm


def _best_candidate(paper_value: str, candidates: list[str]) -> tuple[str | None, str]:
    """Compare paper_value against candidates; returns (best_match, 'exact' | 'partial' | 'none')."""
    paper_core = normalize_core(paper_value)
    best: str | None = None
    best_kind = "none"
    for candidate in candidates:
        candidate_core = normalize_core(candidate)
        if candidate_core == paper_core:
            return candidate, "exact"
        if best_kind == "none" and (paper_core in candidate_core or candidate_core in paper_core):
            best, best_kind = candidate, "partial"
    return best, best_kind


def compare_single(item_label: str, paper_field: dict, candidates: list[str]) -> dict:
    """Compare a single-value paper component (model/backbone/dataset/loss/optimizer) against
    a list of detected code candidates for that field."""
    paper_value = paper_field["value"]
    paper_found = paper_field["found"]
    code_display = ", ".join(candidates) if candidates else "Not found in code"

    if not paper_found and not candidates:
        return {
            "item": item_label,
            "paper": "Not found in paper",
            "code": code_display,
            "status": STATUS_UNKNOWN,
            "confidence": "Low",
            "explanation": f"{item_label} was not found in either the paper or the code.",
        }

    if not paper_found:
        return {
            "item": item_label,
            "paper": "Not found in paper",
            "code": code_display,
            "status": STATUS_CODE_ONLY,
            "confidence": "Medium",
            "explanation": f"{item_label} was detected in the code ({code_display}) but not identified in the paper.",
        }

    if not candidates:
        return {
            "item": item_label,
            "paper": paper_value,
            "code": code_display,
            "status": STATUS_PAPER_ONLY,
            "confidence": paper_field["confidence"],
            "explanation": f"The paper specifies {paper_value}, but no matching evidence was found in the code.",
        }

    best, kind = _best_candidate(paper_value, candidates)

    if kind == "exact" and len(candidates) == 1:
        return {
            "item": item_label,
            "paper": paper_value,
            "code": code_display,
            "status": STATUS_MATCH,
            "confidence": "High",
            "explanation": f"{paper_value} in the paper matches {best} found in the code.",
        }

    if kind == "exact":
        return {
            "item": item_label,
            "paper": paper_value,
            "code": code_display,
            "status": STATUS_PARTIAL,
            "confidence": "Medium",
            "explanation": (
                f"{paper_value} matches {best} in the code, but additional candidates were "
                f"also found ({code_display})."
            ),
        }

    if kind == "partial":
        return {
            "item": item_label,
            "paper": paper_value,
            "code": code_display,
            "status": STATUS_PARTIAL,
            "confidence": "Low",
            "explanation": f"{paper_value} in the paper is only partially related to {best} found in the code.",
        }

    return {
        "item": item_label,
        "paper": paper_value,
        "code": code_display,
        "status": STATUS_MISMATCH,
        "confidence": "High",
        "explanation": f"The paper specifies {paper_value}, but the code uses {code_display}, which appears unrelated.",
    }


def compare_metrics(paper_field: dict, code_metrics: list[str]) -> dict:
    paper_values = paper_field["value"] if paper_field["found"] else []
    paper_set = {normalize_core(v) for v in paper_values}
    code_set = {normalize_core(v) for v in code_metrics}
    paper_display = ", ".join(paper_values) if paper_values else "Not found in paper"
    code_display = ", ".join(code_metrics) if code_metrics else "Not found in code"

    if not paper_set and not code_set:
        return {
            "item": "Metrics",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_UNKNOWN,
            "confidence": "Low",
            "explanation": "Metrics were not found in either the paper or the code.",
        }

    if not paper_set:
        return {
            "item": "Metrics",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_CODE_ONLY,
            "confidence": "Medium",
            "explanation": f"Metrics found in the code ({code_display}) were not identified in the paper.",
        }

    if not code_set:
        return {
            "item": "Metrics",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_PAPER_ONLY,
            "confidence": paper_field["confidence"],
            "explanation": f"The paper reports {paper_display}, but no matching metrics were found in the code.",
        }

    overlap = paper_set & code_set
    if overlap == paper_set == code_set:
        return {
            "item": "Metrics",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_MATCH,
            "confidence": "High",
            "explanation": f"All reported metrics ({paper_display}) match the code ({code_display}).",
        }

    if overlap:
        return {
            "item": "Metrics",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_PARTIAL,
            "confidence": "Medium",
            "explanation": (
                f"Some metrics overlap between the paper ({paper_display}) and the code "
                f"({code_display}), but not all."
            ),
        }

    return {
        "item": "Metrics",
        "paper": paper_display,
        "code": code_display,
        "status": STATUS_MISMATCH,
        "confidence": "Medium",
        "explanation": f"The paper reports {paper_display}, but the code reports different metrics ({code_display}).",
    }


def _numeric_equal(a: str, b: str) -> bool:
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return a == b


def compare_hyperparameters(paper_field: dict, code_config: dict) -> dict:
    paper_values = paper_field["value"] if paper_field["found"] else {}
    paper_display = ", ".join(f"{k}={v}" for k, v in paper_values.items()) if paper_values else "Not found in paper"
    code_display = ", ".join(f"{k}={v}" for k, v in code_config.items()) if code_config else "Not found in code"

    if not paper_values and not code_config:
        return {
            "item": "Hyperparameters",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_UNKNOWN,
            "confidence": "Low",
            "explanation": "Hyperparameters were not found in either the paper or the code.",
        }

    if not paper_values:
        return {
            "item": "Hyperparameters",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_CODE_ONLY,
            "confidence": "Medium",
            "explanation": f"Hyperparameters found in the code ({code_display}) were not identified in the paper.",
        }

    if not code_config:
        return {
            "item": "Hyperparameters",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_PAPER_ONLY,
            "confidence": paper_field["confidence"],
            "explanation": f"The paper specifies {paper_display}, but no matching configuration was found in the code.",
        }

    common_keys = set(paper_values) & set(code_config)
    if not common_keys:
        return {
            "item": "Hyperparameters",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_MISMATCH,
            "confidence": "Low",
            "explanation": (
                f"The paper specifies {paper_display} and the code specifies {code_display}, "
                "but no comparable keys overlap."
            ),
        }

    matching_keys = [k for k in common_keys if _numeric_equal(paper_values[k], code_config[k])]

    if len(matching_keys) == len(common_keys) == len(paper_values) == len(code_config):
        return {
            "item": "Hyperparameters",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_MATCH,
            "confidence": "High",
            "explanation": f"All hyperparameters match between the paper ({paper_display}) and the code ({code_display}).",
        }

    if matching_keys:
        return {
            "item": "Hyperparameters",
            "paper": paper_display,
            "code": code_display,
            "status": STATUS_PARTIAL,
            "confidence": "Medium",
            "explanation": (
                f"Some hyperparameters match ({', '.join(matching_keys)}), but others differ "
                "between the paper and the code."
            ),
        }

    return {
        "item": "Hyperparameters",
        "paper": paper_display,
        "code": code_display,
        "status": STATUS_MISMATCH,
        "confidence": "Medium",
        "explanation": f"The paper specifies {paper_display}, but the code specifies different values ({code_display}).",
    }


def compare_paper_and_code(components: dict, code_hints: dict) -> list[dict]:
    """
    Build a list of dicts matching the ComparisonItem schema by comparing
    extracted paper Components against extracted repository CodeHints.
    """
    return [
        compare_single("Model", components["model"], code_hints["models"]),
        compare_single("Backbone", components["backbone"], code_hints["backbones"]),
        compare_single("Dataset", components["dataset"], code_hints["datasets"]),
        compare_single("Loss Function", components["loss"], code_hints["losses"]),
        compare_single("Optimizer", components["optimizer"], code_hints["optimizers"]),
        compare_metrics(components["metrics"], code_hints["metrics"]),
        compare_hyperparameters(components["hyperparameters"], code_hints["config"]),
    ]
