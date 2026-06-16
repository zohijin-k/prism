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

# Which sections to check first per field (falls back to all remaining sections, then full text)
SECTION_PRIORITY = {
    "dataset": ["experiments", "results", "method"],
    "model": ["method", "introduction", "abstract"],
    "backbone": ["method", "experiments"],
    "loss": ["method", "experiments"],
    "optimizer": ["experiments", "method"],
    "metrics": ["experiments", "results"],
    "hyperparameters": ["experiments"],
}

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


def _display(term: str) -> str:
    return DISPLAY_NAMES.get(term, term.title())


def _ordered_section_texts(sections: dict, field: str) -> list[tuple[str, str]]:
    """[(section_key, body), ...] in priority order for *field*, then any remaining sections."""
    priority = SECTION_PRIORITY.get(field, [])
    seen = set()
    ordered = []
    for key in priority:
        if key in sections:
            ordered.append((key, sections[key]["body"]))
            seen.add(key)
    for key, info in sections.items():
        if key not in seen:
            ordered.append((key, info["body"]))
    return ordered


def _find_known_term(sections: dict, field: str, terms: list[str], full_text: str) -> Optional[dict]:
    for key, body in _ordered_section_texts(sections, field):
        lowered = body.lower()
        for term in terms:
            if term in lowered:
                return {"value": _display(term), "source": key, "confidence": "High", "found": True}
    lowered_full = full_text.lower()
    for term in terms:
        if term in lowered_full:
            return {"value": _display(term), "source": None, "confidence": "Medium", "found": True}
    return None


def _extract_dataset(sections: dict, full_text: str) -> Optional[dict]:
    known = _find_known_term(sections, "dataset", KNOWN_DATASETS, full_text)
    if known:
        return known
    for key, body in _ordered_section_texts(sections, "dataset"):
        m = DATASET_CONTEXT_RE.search(body) or DATASET_SUFFIX_RE.search(body)
        if m:
            return {"value": f"{m.group(1)} dataset", "source": key, "confidence": "Medium", "found": True}
    m = DATASET_CONTEXT_RE.search(full_text) or DATASET_SUFFIX_RE.search(full_text)
    if m:
        return {"value": f"{m.group(1)} dataset", "source": None, "confidence": "Low", "found": True}
    return None


def _extract_metrics(sections: dict, full_text: str) -> Optional[dict]:
    for key, body in _ordered_section_texts(sections, "metrics"):
        lowered = body.lower()
        matched = [_display(t) for t in KNOWN_METRICS if t in lowered]
        if matched:
            # de-dupe while preserving order
            seen = set()
            unique = [m for m in matched if not (m in seen or seen.add(m))]
            return {"value": unique, "source": key, "confidence": "High", "found": True}

    lowered_full = full_text.lower()
    matched = [_display(t) for t in KNOWN_METRICS if t in lowered_full]
    if matched:
        seen = set()
        unique = [m for m in matched if not (m in seen or seen.add(m))]
        return {"value": unique, "source": None, "confidence": "Medium", "found": True}
    return None


def _extract_hyperparameters(sections: dict, full_text: str) -> Optional[dict]:
    for key, body in _ordered_section_texts(sections, "hyperparameters"):
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
            return {"value": values, "source": key, "confidence": confidence, "found": True}

    values = {}
    lr, bs, ep = LR_RE.search(full_text), BATCH_RE.search(full_text), EPOCH_RE.search(full_text)
    if lr:
        values["learningRate"] = lr.group(1)
    if bs:
        values["batchSize"] = bs.group(1)
    if ep:
        values["epochs"] = ep.group(1)
    if values:
        return {"value": values, "source": None, "confidence": "Medium", "found": True}
    return None


def extract_components(parsed: Optional[dict]) -> dict:
    """
    Build a dict matching the Components schema (each field wrapped with
    value/source/confidence/found) from a parse_pdf() result, or None if
    PDF parsing failed entirely. Falls back to FALLBACK_DEFAULTS per-field
    when nothing is found, with found=False and confidence="Low".
    """
    sections = parsed["sections"] if parsed else {}
    full_text = parsed["full_text"] if parsed else ""

    def with_fallback(extracted: Optional[dict], default_value) -> dict:
        if extracted:
            return extracted
        return {"value": default_value, "source": None, "confidence": "Low", "found": False}

    return {
        "dataset": with_fallback(_extract_dataset(sections, full_text), FALLBACK_DEFAULTS["dataset"]),
        "model": with_fallback(_find_known_term(sections, "model", KNOWN_MODELS, full_text), FALLBACK_DEFAULTS["model"]),
        "backbone": with_fallback(_find_known_term(sections, "backbone", KNOWN_BACKBONES, full_text), FALLBACK_DEFAULTS["backbone"]),
        "loss": with_fallback(_find_known_term(sections, "loss", KNOWN_LOSSES, full_text), FALLBACK_DEFAULTS["loss"]),
        "optimizer": with_fallback(_find_known_term(sections, "optimizer", KNOWN_OPTIMIZERS, full_text), FALLBACK_DEFAULTS["optimizer"]),
        "metrics": with_fallback(_extract_metrics(sections, full_text), FALLBACK_DEFAULTS["metrics"]),
        "hyperparameters": with_fallback(_extract_hyperparameters(sections, full_text), FALLBACK_DEFAULTS["hyperparameters"]),
    }
