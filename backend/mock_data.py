from component_extractor import FALLBACK_DEFAULTS
from models.schemas import AnalysisResult
from repo_analyzer import EMPTY_CODE_HINTS

# paperInfo, components, repoAnalysis, comparison, and mapping below are placeholders only:
# routers/analyze.py always overrides them with real extraction/analysis results before
# returning a response, so their literal content never reaches a client. summary,
# implementationPlan, and missingInfo are the only fields still served as-is (no real
# analysis engine for those yet).
MOCK_RESULT = AnalysisResult(
    summary={
        "problem": "This paper addresses the difficulty of accurately segmenting small objects in complex visual scenes.",
        "limitation": "Existing encoder-decoder architectures often lose fine-grained boundary information.",
        "method": "The proposed method introduces an attention-based skip connection module to preserve important spatial features.",
        "result": "The method improves Dice Score and mIoU compared to the baseline U-Net architecture.",
        "contribution": [
            "Attention-based feature refinement",
            "Improved boundary preservation",
            "Better reproducibility through modular architecture",
        ],
    },
    implementationPlan=[
        "Prepare dataset and define preprocessing pipeline",
        "Implement encoder-decoder model architecture",
        "Add attention module to skip connections",
        "Implement Dice Loss and BCE Loss",
        "Write training loop and validation loop",
        "Evaluate using Dice Score and mIoU",
        "Compare reproduced results with paper tables",
    ],
    components={
        key: {"value": value, "source": None, "confidence": "Low", "found": False}
        for key, value in FALLBACK_DEFAULTS.items()
    },
    repoAnalysis={
        "inputType": "none",
        "repoName": None,
        "status": "No repository or code provided",
        "relevantFiles": [],
        "fileCount": 0,
        "codeHints": EMPTY_CODE_HINTS,
    },
    comparison=[],
    mapping=[],
    missingInfo=[
        "Random seed is not specified in the paper.",
        "Learning rate scheduler is not clearly described.",
        "Detailed augmentation policy is missing.",
        "Pretrained weight usage is unclear.",
        "Exact GPU environment is not provided.",
    ],
)
