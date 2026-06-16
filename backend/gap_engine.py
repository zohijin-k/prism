from __future__ import annotations

SEED_KEYWORDS = ["random seed", "manual_seed", "set_seed", "seed =", "seed=", "np.random.seed"]
SCHEDULER_KEYWORDS = ["scheduler", "cosine annealing", "step decay", "warmup", "lr decay", "learning rate decay"]
AUGMENTATION_KEYWORDS = [
    "augmentation", "random flip", "random crop", "random rotation", "color jitter", "mixup", "cutmix",
]
PRETRAINED_KEYWORDS = ["pretrained", "pre-trained", "fine-tuned from", "initialized from"]
HARDWARE_KEYWORDS = ["gpu", "nvidia", "rtx", "v100", "a100", "tpu", "cuda"]


def _any_present(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in keywords)


def detect_gaps(full_text: str, components: dict) -> list[str]:
    """
    Detect reproducibility gaps by scanning the paper's full text for known keywords and
    checking extracted hyperparameters. Only items that appear missing are reported —
    nothing is reported just because it's "usually" missing.
    """
    lowered = full_text.lower()
    gaps: list[str] = []

    if not _any_present(lowered, SEED_KEYWORDS):
        gaps.append("Random Seed 정보가 명시되지 않았습니다.")

    if not _any_present(lowered, SCHEDULER_KEYWORDS):
        gaps.append("Learning Rate Scheduler 설정이 확인되지 않습니다.")

    if not _any_present(lowered, AUGMENTATION_KEYWORDS):
        gaps.append("데이터 증강(Augmentation) 기법에 대한 정보가 명시되지 않았습니다.")

    if not _any_present(lowered, PRETRAINED_KEYWORDS):
        gaps.append("사전 학습된(Pretrained) 가중치 사용 여부가 명확하지 않습니다.")

    if not _any_present(lowered, HARDWARE_KEYWORDS):
        gaps.append("학습에 사용된 GPU 환경 정보가 제공되지 않습니다.")

    hyperparameters = components["hyperparameters"]
    hp = hyperparameters["value"] if hyperparameters["found"] else {}

    if not hp.get("epochs"):
        gaps.append("학습 Epoch 수가 명확히 제시되지 않았습니다.")
    if not hp.get("batchSize"):
        gaps.append("Batch Size 정보가 명시되지 않았습니다.")
    if not hp.get("learningRate"):
        gaps.append("Learning Rate 값이 명확히 제시되지 않았습니다.")

    return gaps
