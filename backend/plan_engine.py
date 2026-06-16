from __future__ import annotations

MIN_STEPS = 5
MAX_STEPS = 8

GENERIC_FILLERS = [
    "코드 구조 설계 및 모듈화",
    "실험 환경 설정 및 재현성 점검",
    "데이터 증강 및 정규화 기법 적용 검토",
]


def generate_plan(components: dict) -> list[str]:
    """
    Build an ordered list of Korean implementation steps from extracted paper Components.
    Only emits a step for a field when it was actually found in the paper (found=True) —
    fields still on their fallback default are skipped entirely, so the plan never reflects
    a hardcoded workflow for a paper that didn't specify that component.
    """
    dataset = components["dataset"]
    model = components["model"]
    backbone = components["backbone"]
    loss = components["loss"]
    optimizer = components["optimizer"]
    metrics = components["metrics"]
    hyperparameters = components["hyperparameters"]

    steps: list[str] = []

    if dataset["found"]:
        steps.append(f"{dataset['value']} 데이터셋 준비 및 전처리")

    if model["found"] and backbone["found"]:
        steps.append(f"{backbone['value']} 백본을 적용한 {model['value']} 모델 구조 구현")
    elif model["found"]:
        steps.append(f"{model['value']} 기반 모델 구조 구현")
    elif backbone["found"]:
        steps.append(f"{backbone['value']} 백본 기반 모델 구조 구현")

    if loss["found"]:
        steps.append(f"{loss['value']} 손실 함수 구현")

    hp = hyperparameters["value"] if hyperparameters["found"] else {}
    if optimizer["found"]:
        if hp.get("learningRate"):
            steps.append(f"{optimizer['value']} Optimizer 설정 (learning rate={hp['learningRate']})")
        else:
            steps.append(f"{optimizer['value']} Optimizer 설정")
    elif hp:
        steps.append("주요 하이퍼파라미터 설정")

    steps.append("학습 파이프라인 및 검증 루프 구축")

    if metrics["found"] and metrics["value"]:
        steps.append(f"{', '.join(metrics['value'])} 평가 지표 구현")

    filler_idx = 0
    while len(steps) < MIN_STEPS - 1 and filler_idx < len(GENERIC_FILLERS):
        steps.append(GENERIC_FILLERS[filler_idx])
        filler_idx += 1

    steps = steps[: MAX_STEPS - 1]
    steps.append("논문 결과 재현 및 비교")

    return steps
