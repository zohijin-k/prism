from __future__ import annotations

import re
from typing import Optional

# Default values used when nothing is found in the paper (mirrors the original mock)
FALLBACK_DEFAULTS = {
    "dataset": "Medical image segmentation dataset",
    "model": "Attention U-Net",
    "backbone": "U-Net encoder-decoder",
    "loss": "Dice Loss + BCE Loss",
    "optimizer": "Adam",
    "metrics": ["Dice Score", "mIoU"],
    "hyperparameters": {"learningRate": "1e-4", "batchSize": "8", "epochs": "100"},
    "task": "Not specified in title",
}

# Known terms, most specific first so multi-word matches win over generic substrings
KNOWN_MODELS = [
    "attention u-net", "u-net", "unet", "mask r-cnn", "faster r-cnn",
    "vision transformer", "swin transformer", "resnet", "transformer",
    "vgg", "efficientnet", "vit", "bert", "gpt", "yolo", "lstm", "gru",
    "gan", "autoencoder", "cnn",
]
KNOWN_BACKBONES = [
    "efficientnet", "resnet", "vgg", "mobilenet", "densenet", "inception",
    "swin transformer", "vit", "xception",
]
KNOWN_LOSSES = [
    "dice loss", "dice bce", "binary cross entropy", "bce loss",
    "cross entropy loss", "cross entropy", "mean squared error", "mse loss",
    "focal loss", "l1 loss", "l2 loss", "hinge loss", "huber loss",
]
KNOWN_OPTIMIZERS = ["adamw", "adam", "sgd", "rmsprop", "adagrad", "adadelta"]
KNOWN_METRICS = [
    "miou", "mean iou", "dice score", "dice coefficient", "accuracy",
    "f1-score", "f1 score", "precision", "recall", "auc", "psnr", "ssim",
    "bleu", "rouge",
]
KNOWN_DATASETS = [
    "pascal voc", "ms coco", "coco", "imagenet", "cifar-10", "cifar-100",
    "mnist", "cityscapes", "ade20k", "kitti", "brats", "isic", "celeba",
    "squad", "glue", "wikitext", "librispeech", "ucf101", "kinetics",
]

DISPLAY_NAMES = {
    "attention u-net": "Attention U-Net", "u-net": "U-Net", "unet": "U-Net",
    "mask r-cnn": "Mask R-CNN", "faster r-cnn": "Faster R-CNN",
    "vision transformer": "Vision Transformer", "swin transformer": "Swin Transformer",
    "resnet": "ResNet", "transformer": "Transformer", "vgg": "VGG",
    "efficientnet": "EfficientNet", "vit": "ViT", "bert": "BERT", "gpt": "GPT",
    "yolo": "YOLO", "lstm": "LSTM", "gru": "GRU", "gan": "GAN",
    "autoencoder": "Autoencoder", "cnn": "CNN", "mobilenet": "MobileNet",
    "densenet": "DenseNet", "inception": "Inception", "xception": "Xception",
    "dice loss": "Dice Loss", "dice bce": "Dice BCE Loss",
    "binary cross entropy": "Binary Cross Entropy", "bce loss": "BCE Loss",
    "cross entropy loss": "Cross Entropy Loss", "cross entropy": "Cross Entropy",
    "mean squared error": "Mean Squared Error", "mse loss": "MSE Loss",
    "focal loss": "Focal Loss", "l1 loss": "L1 Loss", "l2 loss": "L2 Loss",
    "hinge loss": "Hinge Loss", "huber loss": "Huber Loss",
    "adamw": "AdamW", "adam": "Adam", "sgd": "SGD", "rmsprop": "RMSprop",
    "adagrad": "Adagrad", "adadelta": "Adadelta",
    "miou": "mIoU", "mean iou": "Mean IoU", "dice score": "Dice Score",
    "dice coefficient": "Dice Coefficient", "accuracy": "Accuracy",
    "f1-score": "F1-Score", "f1 score": "F1 Score", "precision": "Precision",
    "recall": "Recall", "auc": "AUC", "psnr": "PSNR", "ssim": "SSIM",
    "bleu": "BLEU", "rouge": "ROUGE",
    "pascal voc": "PASCAL VOC", "ms coco": "MS COCO", "coco": "COCO",
    "imagenet": "ImageNet", "cifar-10": "CIFAR-10", "cifar-100": "CIFAR-100",
    "mnist": "MNIST", "cityscapes": "Cityscapes", "ade20k": "ADE20K",
    "kitti": "KITTI", "brats": "BraTS", "isic": "ISIC", "celeba": "CelebA",
    "squad": "SQuAD", "glue": "GLUE", "wikitext": "WikiText",
    "librispeech": "LibriSpeech", "ucf101": "UCF101", "kinetics": "Kinetics",
}

# How much each section counts toward a component's extraction score. Title/Abstract/Method
# describe what the paper actually proposes; Related Work mostly cites comparison baselines,
# so it's weighted lowest to avoid those baselines being mistaken for the paper's own
# components.
SECTION_WEIGHTS = {
    "abstract": 8,
    "method": 7,
    "implementation_details": 6,
    "experiments": 5,
    "results": 4,
    "introduction": 2,
    "related_work": 1,
}
DEFAULT_SECTION_WEIGHT = 2  # conclusion and any other unlisted section
TITLE_WEIGHT = 10  # synthetic "title" source — highest priority for naming the model

# Sections that legitimately describe the paper's own training setup. Optimizer must be
# confirmed here — a mention in Related Work or Introduction is not "this paper's optimizer".
OPTIMIZER_SECTIONS = ("method", "experiments", "implementation_details")

DATASET_CONTEXT_RE = re.compile(
    r"(?:trained on|evaluated on|on the|using the)\s+(?:the\s+)?"
    r"([A-Za-z][\w\-]*(?:\s+[A-Za-z][\w\-]*){0,3})\s+dataset",
    re.IGNORECASE,
)
DATASET_SUFFIX_RE = re.compile(
    r"([A-Za-z][\w\-]*(?:\s+[A-Za-z][\w\-]*){0,3})\s+dataset", re.IGNORECASE
)
LR_RE = re.compile(r"learning rate[^0-9]{0,12}([0-9]+\.?[0-9]*(?:e-?[0-9]+)?)", re.IGNORECASE)
BATCH_RE = re.compile(r"batch size[^0-9]{0,12}([0-9]+)", re.IGNORECASE)
EPOCH_RE = re.compile(r"([0-9]+)\s+epochs", re.IGNORECASE)

# A single word of a proper-noun model name, hyphen-tolerant ("Pre-training", "Language-Image")
_NAME_WORD = r"[A-Z][a-zA-Z]+(?:-[A-Za-z0-9]+)*"
# A 1-4 word Title-Case model name ("DCPNet", "Segment Anything", "Vision Transformer")
_NAME_PHRASE = rf"{_NAME_WORD}(?:\s{_NAME_WORD}){{0,3}}"

# "Long Descriptive Name (ACRONYM)" — the most common way papers define their own model name
LONGNAME_ACRONYM_RE = re.compile(
    rf"\b({_NAME_WORD}(?:\s{_NAME_WORD}){{1,5}})\s*\(([A-Z][A-Za-z0-9\-]{{1,15}})\)"
)
# "ACRONYM (Long Descriptive Name)" — the reversed convention (e.g. CLIP papers)
ACRONYM_LONGNAME_RE = re.compile(
    rf"\b([A-Z]{{2,10}})\s*\(({_NAME_WORD}(?:\s{_NAME_WORD}){{1,6}})\)"
)
# "we propose/introduce/present/call/name/term ... <Name>", plus common paraphrasings like
# "our proposed/network/framework/architecture" and "the proposed method/model"
PROPOSED_NAME_RE = re.compile(
    r"\b(?:[Ww]e\s+(?:propose|introduce|present|call|name|term)|"
    r"[Tt]his\s+(?:paper|work)\s+(?:proposes|introduces|presents)|"
    r"[Oo]ur\s+(?:proposed|network|framework|architecture)|"
    r"[Tt]he\s+proposed\s+(?:method|model)|"
    r"introduced\s+in\s+this\s+paper)"
    rf"[^.]{{0,80}}?\b({_NAME_PHRASE})\b"
)
# Paper titles conventionally read "ModelName: longer description [for <task>]". The title's
# own name token is more lenient than _NAME_WORD — short hyphenated names like "U-Net" or
# "R-CNN" have fewer than 2 letters before the hyphen, which _NAME_WORD's "1+ letters" rule
# would otherwise reject.
_TITLE_NAME_WORD = r"[A-Z][a-zA-Z0-9]*(?:-[A-Za-z0-9]+)*"
TITLE_COLON_RE = re.compile(rf"^\s*({_TITLE_NAME_WORD})\s*:\s+(\S.*)$")
# Generic "XyzNet"-style architecture token, used as a last-resort signal when it repeats in Method
ARCH_TOKEN_RE = re.compile(r"\b([A-Z][a-zA-Z0-9]{1,12}Net)\b")
ARCH_TOKEN_BLOCKLIST = {"imagenet", "internet", "subnet", "intranet", "resnet", "unet"}

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _display(term: str) -> str:
    return DISPLAY_NAMES.get(term, term.title())


def _matched_sentence(body: str, term: str) -> Optional[str]:
    """First sentence in *body* containing *term* (case-insensitive), trimmed for display."""
    if not body or not term:
        return None
    lowered_term = term.lower()
    for sentence in _SENTENCE_SPLIT_RE.split(body):
        if lowered_term in sentence.lower():
            return sentence.strip()[:240]
    return body.strip()[:240] or None


def _title_guess(full_text: str) -> str:
    """
    Best-effort guess at the paper title. _detect_sections() discards everything before
    the first recognised header, so the title never makes it into `sections` — recover it
    here as the first few non-empty lines before the Abstract.
    """
    idx = full_text.lower().find("abstract")
    preamble = full_text[:idx] if idx != -1 else full_text[:300]
    lines = [line.strip() for line in preamble.splitlines() if line.strip()]
    return " ".join(lines[:3])


def _sections_by_weight(sections: dict) -> list[tuple[str, str]]:
    """All sections as (key, body), ordered from highest extraction weight to lowest."""
    items = sorted(sections.items(), key=lambda kv: -SECTION_WEIGHTS.get(kv[0], DEFAULT_SECTION_WEIGHT))
    return [(key, info["body"]) for key, info in items]


def _score_known_terms(sections: dict, terms: list[str]) -> dict[str, dict]:
    """
    Score every known *term* found anywhere in *sections* by section weight, with a capped
    bonus for repeated mentions within the same section. Returns the single best-scoring
    occurrence per term: {term: {"score", "section", "sentence"}}.
    """
    candidates: dict[str, dict] = {}
    for key, info in sections.items():
        body = info["body"]
        lowered = body.lower()
        weight = SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT)
        for term in terms:
            count = lowered.count(term)
            if not count:
                continue
            score = weight * min(count, 3)
            existing = candidates.get(term)
            if existing is None or score > existing["score"]:
                candidates[term] = {"score": score, "section": key, "sentence": _matched_sentence(body, term)}
    return candidates


def _best_known_term(sections: dict, terms: list[str], full_text: str, min_weight: int = 1) -> Optional[dict]:
    """
    Pick the highest-scoring known term across *sections*. `min_weight` filters out terms
    whose only evidence comes from low-priority sections — e.g. min_weight=2 means a term
    that appears solely in Related Work (weight 1) is ignored entirely. Only falls back to
    a blind full-text scan when min_weight allows any section (min_weight<=1), since that
    fallback can't distinguish which section a match came from.
    """
    candidates = _score_known_terms(sections, terms)
    qualifying = {
        term: c for term, c in candidates.items()
        if SECTION_WEIGHTS.get(c["section"], DEFAULT_SECTION_WEIGHT) >= min_weight
    }
    if qualifying:
        term, best = max(qualifying.items(), key=lambda kv: kv[1]["score"])
        return {
            "value": _display(term),
            "source": best["section"],
            "confidence": "High",
            "found": True,
            "matchedSentence": best["sentence"],
            "score": best["score"],
        }

    if min_weight <= 1:
        lowered_full = full_text.lower()
        for term in terms:
            if term in lowered_full:
                return {
                    "value": _display(term),
                    "source": None,
                    "confidence": "Medium",
                    "found": True,
                    "matchedSentence": _matched_sentence(full_text, term),
                    "score": DEFAULT_SECTION_WEIGHT,
                }
    return None


def _find_repeated_method_architecture(sections: dict) -> Optional[dict]:
    """Last-resort model signal: an unlisted 'XyzNet'-style token mentioned 2+ times in Method."""
    method_body = sections.get("method", {}).get("body", "")
    if not method_body:
        return None
    counts: dict[str, int] = {}
    for match in ARCH_TOKEN_RE.finditer(method_body):
        token = match.group(1)
        if token.lower() in ARCH_TOKEN_BLOCKLIST:
            continue
        counts[token] = counts.get(token, 0) + 1
    qualifying = {token: count for token, count in counts.items() if count >= 2}
    if not qualifying:
        return None
    token = max(qualifying, key=qualifying.get)
    return {
        "value": token,
        "source": "method",
        "confidence": "Medium",
        "found": True,
        "matchedSentence": _matched_sentence(method_body, token),
        "score": SECTION_WEIGHTS["method"] * min(qualifying[token], 3),
    }


def _find_proposed_model_name(sections: dict, full_text: str) -> Optional[dict]:
    """
    Look for the paper's own proposed model name, never Related Work: the title's
    'Name: Expanded Description [for Task]' convention, an explicit acronym definition
    (either 'Long Descriptive Name (ACRONYM)' or the reversed 'ACRONYM (Long Descriptive
    Name)'), 'we propose/introduce ... <Name>' phrasing, then a repeated architecture-style
    token in Method. Title is checked first since it names the model with full authority
    before the body is scanned at all.
    """
    title = _title_guess(full_text)
    m = TITLE_COLON_RE.match(title)
    if m:
        name, rest = m.group(1), m.group(2).strip()
        task_split = re.split(r"\bfor\b", rest, maxsplit=1, flags=re.IGNORECASE)
        expanded = task_split[0].strip().rstrip(",.:;") or None
        return {
            "value": name,
            "source": "title",
            "confidence": "High",
            "found": True,
            "matchedSentence": title[:240],
            "score": TITLE_WEIGHT,
            "expandedName": expanded,
        }

    search_order = [
        ("abstract", sections.get("abstract", {}).get("body", "")),
        ("method", sections.get("method", {}).get("body", "")),
        ("introduction", sections.get("introduction", {}).get("body", "")),
    ]

    for key, body in search_order:
        if not body:
            continue
        m = LONGNAME_ACRONYM_RE.search(body)
        if m:
            expanded, acronym = m.group(1), m.group(2)
            weight = SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT)
            return {
                "value": acronym,
                "source": key,
                "confidence": "High",
                "found": True,
                "matchedSentence": m.group(0).strip()[:240],
                "score": weight + 10,
                "expandedName": expanded,
            }
        m = ACRONYM_LONGNAME_RE.search(body)
        if m:
            acronym, expanded = m.group(1), m.group(2)
            weight = SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT)
            return {
                "value": acronym,
                "source": key,
                "confidence": "High",
                "found": True,
                "matchedSentence": m.group(0).strip()[:240],
                "score": weight + 10,
                "expandedName": expanded,
            }

    for key, body in search_order:
        if not body:
            continue
        m = PROPOSED_NAME_RE.search(body)
        if m:
            name = m.group(1)
            weight = SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT)
            return {
                "value": name,
                "source": key,
                "confidence": "High",
                "found": True,
                "matchedSentence": _matched_sentence(body, name) or m.group(0).strip()[:240],
                "score": weight + 8,
            }

    return _find_repeated_method_architecture(sections)


def _extract_task(full_text: str) -> Optional[dict]:
    """
    Recover the paper's task/domain from the title's 'Name: Description for Task' convention
    (e.g. "... for Image Enhancement"). Only the title is authoritative enough for this —
    body text doesn't reliably state the task in one phrase.
    """
    title = _title_guess(full_text)
    m = TITLE_COLON_RE.match(title)
    if not m:
        return None
    rest = m.group(2).strip()
    parts = re.split(r"\bfor\b", rest, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) < 2:
        return None
    task = parts[1].strip().rstrip(".,;:")
    if not task:
        return None
    return {
        "value": task,
        "source": "title",
        "confidence": "High",
        "found": True,
        "matchedSentence": title[:240],
        "score": TITLE_WEIGHT,
    }


def _extract_referenced_models(sections: dict, primary_model_value: Optional[str]) -> list[str]:
    """
    Known models whose only evidence is Related Work (weight 1) — comparison baselines the
    paper cites but doesn't propose. Excluded if it matches the chosen primary model, so the
    proposed model itself never double-lists as a "reference".
    """
    candidates = _score_known_terms(sections, KNOWN_MODELS)
    primary_lower = (primary_model_value or "").lower()
    referenced = []
    for term, info in candidates.items():
        if info["section"] != "related_work":
            continue
        if term == primary_lower or _display(term).lower() == primary_lower:
            continue
        referenced.append(_display(term))
    return sorted(set(referenced))


def _extract_optimizer(sections: dict) -> Optional[dict]:
    """
    Optimizer must be confirmed in the paper's own training/experiment description
    (Method or Experiments — the latter's aliases already cover "Implementation Details").
    Unlike other fields, this never falls back to Related Work, Introduction, or a blind
    full-text scan, so a citation like "...unlike SGD used in [12]..." can't be inferred
    as this paper's optimizer.
    """
    restricted = {k: v for k, v in sections.items() if k in OPTIMIZER_SECTIONS}
    candidates = _score_known_terms(restricted, KNOWN_OPTIMIZERS)
    if not candidates:
        return None
    term, best = max(candidates.items(), key=lambda kv: kv[1]["score"])
    return {
        "value": _display(term),
        "source": best["section"],
        "confidence": "High",
        "found": True,
        "matchedSentence": best["sentence"],
        "score": best["score"],
    }


def _extract_dataset(sections: dict, full_text: str) -> Optional[dict]:
    """Datasets only mentioned in Related Work (weight 1) are ignored — require weight >= 2."""
    known = _best_known_term(sections, KNOWN_DATASETS, full_text, min_weight=2)
    if known:
        return known
    for key, body in _sections_by_weight(sections):
        if SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT) < 2:
            continue
        m = DATASET_CONTEXT_RE.search(body) or DATASET_SUFFIX_RE.search(body)
        if m:
            return {
                "value": f"{m.group(1)} dataset",
                "source": key,
                "confidence": "Medium",
                "found": True,
                "matchedSentence": _matched_sentence(body, m.group(1)),
                "score": SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT),
            }
    return None


def _extract_metrics(sections: dict, full_text: str) -> Optional[dict]:
    for key, body in _sections_by_weight(sections):
        lowered = body.lower()
        matched_terms = [t for t in KNOWN_METRICS if t in lowered]
        if matched_terms:
            seen = set()
            unique = [_display(t) for t in matched_terms if not (t in seen or seen.add(t))]
            return {
                "value": unique,
                "source": key,
                "confidence": "High",
                "found": True,
                "matchedSentence": _matched_sentence(body, matched_terms[0]),
                "score": SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT),
            }

    lowered_full = full_text.lower()
    matched_terms = [t for t in KNOWN_METRICS if t in lowered_full]
    if matched_terms:
        seen = set()
        unique = [_display(t) for t in matched_terms if not (t in seen or seen.add(t))]
        return {
            "value": unique,
            "source": None,
            "confidence": "Medium",
            "found": True,
            "matchedSentence": None,
            "score": DEFAULT_SECTION_WEIGHT,
        }
    return None


def _extract_hyperparameters(sections: dict, full_text: str) -> Optional[dict]:
    for key, body in _sections_by_weight(sections):
        values: dict[str, str] = {}
        lr, bs, ep = LR_RE.search(body), BATCH_RE.search(body), EPOCH_RE.search(body)
        if lr:
            values["learningRate"] = lr.group(1)
        if bs:
            values["batchSize"] = bs.group(1)
        if ep:
            values["epochs"] = ep.group(1)
        if values:
            confidence = "High" if len(values) >= 2 else "Medium"
            sentence = _matched_sentence(body, "learning rate" if lr else "batch size" if bs else "epochs")
            return {
                "value": values,
                "source": key,
                "confidence": confidence,
                "found": True,
                "matchedSentence": sentence,
                "score": SECTION_WEIGHTS.get(key, DEFAULT_SECTION_WEIGHT),
            }

    values = {}
    lr, bs, ep = LR_RE.search(full_text), BATCH_RE.search(full_text), EPOCH_RE.search(full_text)
    if lr:
        values["learningRate"] = lr.group(1)
    if bs:
        values["batchSize"] = bs.group(1)
    if ep:
        values["epochs"] = ep.group(1)
    if values:
        return {
            "value": values,
            "source": None,
            "confidence": "Medium",
            "found": True,
            "matchedSentence": None,
            "score": DEFAULT_SECTION_WEIGHT,
        }
    return None


def extract_components(parsed: Optional[dict]) -> dict:
    """
    Build a dict matching the Components schema (each field wrapped with
    value/source/confidence/found/matchedSentence/score) from a parse_pdf() result, or None
    if PDF parsing failed entirely. Falls back to FALLBACK_DEFAULTS per-field when nothing
    is found, with found=False and confidence="Low".

    Method/Experiments/Results are weighted above Introduction/Related Work (see
    SECTION_WEIGHTS) so that components only cited in Related Work — e.g. a baseline the
    paper compares against — aren't mistaken for the paper's own model, dataset, or optimizer.
    """
    sections = parsed["sections"] if parsed else {}
    full_text = parsed["full_text"] if parsed else ""

    def with_fallback(extracted: Optional[dict], default_value) -> dict:
        if extracted:
            return extracted
        return {"value": default_value, "source": None, "confidence": "Low", "found": False}

    proposed_model = _find_proposed_model_name(sections, full_text)
    model = proposed_model or _best_known_term(sections, KNOWN_MODELS, full_text, min_weight=2)
    expanded_model_name = (proposed_model or {}).get("expandedName")

    return {
        "dataset": with_fallback(_extract_dataset(sections, full_text), FALLBACK_DEFAULTS["dataset"]),
        "model": with_fallback(model, FALLBACK_DEFAULTS["model"]),
        "expandedModelName": expanded_model_name,
        "task": with_fallback(_extract_task(full_text), FALLBACK_DEFAULTS["task"]),
        "referencedModels": _extract_referenced_models(sections, model.get("value") if model else None),
        "backbone": with_fallback(
            _best_known_term(sections, KNOWN_BACKBONES, full_text, min_weight=1), FALLBACK_DEFAULTS["backbone"]
        ),
        "loss": with_fallback(
            _best_known_term(sections, KNOWN_LOSSES, full_text, min_weight=1), FALLBACK_DEFAULTS["loss"]
        ),
        "optimizer": with_fallback(_extract_optimizer(sections), FALLBACK_DEFAULTS["optimizer"]),
        "metrics": with_fallback(_extract_metrics(sections, full_text), FALLBACK_DEFAULTS["metrics"]),
        "hyperparameters": with_fallback(_extract_hyperparameters(sections, full_text), FALLBACK_DEFAULTS["hyperparameters"]),
    }
