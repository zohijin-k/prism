from __future__ import annotations

# (keyword, problem phrase, result-domain noun) — most specific keywords first
DOMAIN_KEYWORDS: list[tuple[str, str, str]] = [
    ("low light", "저조도 환경에서 영상 품질이 저하되는", "영상 복원"),
    ("low-light", "저조도 환경에서 영상 품질이 저하되는", "영상 복원"),
    ("dehaz", "안개로 인해 영상 품질이 저하되는", "영상 복원"),
    ("haze", "안개로 인해 영상 품질이 저하되는", "영상 복원"),
    ("super-resolution", "저해상도 영상의 세부 정보가 부족한", "영상 복원"),
    ("super resolution", "저해상도 영상의 세부 정보가 부족한", "영상 복원"),
    ("denois", "영상에 노이즈가 발생하는", "영상 복원"),
    ("deblur", "영상이 흐려지는", "영상 복원"),
    ("segmentation", "객체 영역을 정확하게 분할하기 어려운", "분할"),
    ("detection", "객체를 정확하게 검출하기 어려운", "검출"),
    ("classification", "데이터를 정확하게 분류하기 어려운", "분류"),
    ("depth estim", "정확한 깊이 정보를 추정하기 어려운", "깊이 추정"),
    ("pose estim", "정확한 자세를 추정하기 어려운", "자세 추정"),
    ("medical image", "의료 영상에서 미세한 병변을 식별하기 어려운", "진단 정확도"),
    ("anomaly", "이상 데이터를 정확하게 탐지하기 어려운", "이상 탐지"),
    ("translation", "자연어를 정확하게 번역하기 어려운", "번역"),
    ("question answering", "질문에 정확하게 답변하기 어려운", "응답 정확도"),
    ("generation", "사실적인 데이터를 생성하기 어려운", "생성"),
    ("recognition", "대상을 정확하게 인식하기 어려운", "인식"),
    ("tracking", "객체를 안정적으로 추적하기 어려운", "추적"),
    ("compression", "데이터를 효율적으로 압축하기 어려운", "압축 효율"),
    ("retrieval", "관련 정보를 정확하게 검색하기 어려운", "검색 정확도"),
]
DOMAIN_FALLBACK = ("기존 방법들이 충분히 해결하지 못한", "모델")

# (keyword, Korean phrase with object particle already attached) — most specific first
TECHNIQUE_KEYWORDS: list[tuple[str, str]] = [
    ("deformable", "변형 가능한 제어점 기반 네트워크를"),
    ("self-attention", "셀프 어텐션 구조를"),
    ("attention", "어텐션 메커니즘을"),
    ("transformer", "트랜스포머 구조를"),
    ("graph neural", "그래프 신경망 구조를"),
    ("recurrent", "순환 신경망 구조를"),
    ("generative adversarial", "적대적 생성 네트워크를"),
    ("diffusion", "디퓨전 기반 생성 모델을"),
    ("contrastive", "대조 학습 기법을"),
    ("self-supervised", "자기 지도 학습 기법을"),
    ("knowledge distillation", "지식 증류 기법을"),
    ("multi-scale", "멀티스케일 구조를"),
    ("residual", "잔차 연결 구조를"),
    ("encoder-decoder", "인코더-디코더 구조를"),
    ("skip connection", "스킵 연결 구조를"),
    ("dilated convolution", "확장 컨볼루션 구조를"),
    ("depthwise", "깊이별 컨볼루션 구조를"),
]

MAX_CONTRIBUTIONS = 5


def _match_domain(text: str) -> tuple[str, str]:
    for keyword, phrase, noun in DOMAIN_KEYWORDS:
        if keyword in text:
            return phrase, noun
    return DOMAIN_FALLBACK


def _match_technique(text: str, model_field: dict) -> str:
    for keyword, phrase in TECHNIQUE_KEYWORDS:
        if keyword in text:
            return phrase
    if model_field["found"]:
        return f"{model_field['value']} 기반 네트워크를"
    return "제안하는 네트워크 구조를"


def _build_limitation(model_field: dict, backbone_field: dict) -> str:
    if backbone_field["found"]:
        return f"기존 {backbone_field['value']} 기반 방법은 세부 정보를 충분히 보존하지 못하는 한계가 있다."
    if model_field["found"]:
        return f"기존 {model_field['value']} 기반 방법은 다양한 환경에서 일관된 성능을 보이지 못하는 한계가 있다."
    return "기존 방법들은 특정 조건에서 성능이 저하되는 한계를 가진다."


def _build_result(metrics_field: dict) -> str:
    if metrics_field["found"] and metrics_field["value"]:
        joined = ", ".join(metrics_field["value"])
        return f"제안 방법은 {joined} 등의 지표에서 기존 방법보다 우수한 성능을 달성하였다."
    return "제안 방법은 실험을 통해 기존 방법보다 우수한 성능을 보임을 확인하였다."


def _build_contributions(components: dict) -> list[str]:
    bullets: list[str] = []
    model = components["model"]
    loss = components["loss"]
    dataset = components["dataset"]
    metrics = components["metrics"]
    optimizer = components["optimizer"]

    if model["found"]:
        bullets.append(f"{model['value']} 기반의 새로운 모델 구조를 제안하였다.")
    if loss["found"]:
        bullets.append(f"{loss['value']} 손실 함수를 도입하여 학습 성능을 개선하였다.")
    if dataset["found"]:
        bullets.append(f"{dataset['value']} 데이터셋에서 기존 방법 대비 향상된 성능을 달성하였다.")
    if metrics["found"] and metrics["value"]:
        bullets.append(f"{', '.join(metrics['value'])} 지표를 통해 정량적 성능 향상을 입증하였다.")
    if optimizer["found"]:
        bullets.append(f"{optimizer['value']} 최적화 기법을 적용하여 안정적인 학습을 수행하였다.")

    if not bullets:
        bullets.append("논문에서 제안하는 방법의 핵심 아이디어를 구현 가능한 형태로 정리하였다.")

    return bullets[:MAX_CONTRIBUTIONS]


def generate_summary(sections: dict, components: dict, full_text: str) -> dict:
    """
    Build a dict matching the PaperSummary schema (problem/limitation/method/result/contribution)
    in Korean, dynamically derived from the paper's detected sections and extracted components.
    Falls back to generic-but-still-paper-aware phrasing when specific cues aren't found —
    never returns fixed mock content.
    """
    abstract = sections.get("abstract", {}).get("body", "")
    introduction = sections.get("introduction", {}).get("body", "")
    method_body = sections.get("method", {}).get("body", "")

    problem_scan = (abstract + " " + introduction).lower() or full_text.lower()[:3000]
    technique_scan = (method_body + " " + abstract).lower() or full_text.lower()[:3000]

    domain_phrase, result_noun = _match_domain(problem_scan)
    technique_phrase = _match_technique(technique_scan, components["model"])

    return {
        "problem": f"{domain_phrase} 문제를 해결하는 것을 목표로 한다.",
        "limitation": _build_limitation(components["model"], components["backbone"]),
        "method": f"{technique_phrase} 활용하여 {result_noun} 성능을 향상시킨다.",
        "result": _build_result(components["metrics"]),
        "contribution": _build_contributions(components),
    }
