from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Optional


class SectionInfo(BaseModel):
    header: str
    char_count: int
    preview: str


class PaperSections(BaseModel):
    detected: Dict[str, SectionInfo]  # key = section key e.g. "abstract"
    total_chars: int


class PaperInfo(BaseModel):
    filename: str
    page_count: int
    text_preview: str
    extraction_error: Optional[str] = None
    sections: PaperSections


class PaperSummary(BaseModel):
    problem: str
    limitation: str
    method: str
    result: str
    contribution: List[str]


class Components(BaseModel):
    dataset: str
    model: str
    backbone: str
    loss: str
    optimizer: str
    metrics: List[str]
    hyperparameters: Dict[str, Any]


class ComparisonItem(BaseModel):
    item: str
    paper: str
    code: str
    status: Literal["Match", "Code Only", "Paper Only", "Mismatch"]


class MappingItem(BaseModel):
    codeBlock: str
    paperSection: str
    paperReference: str
    explanation: str
    confidence: Literal["High", "Medium", "Low"]


class AnalysisResult(BaseModel):
    paperInfo: Optional[PaperInfo] = None
    summary: PaperSummary
    implementationPlan: List[str]
    components: Components
    comparison: List[ComparisonItem]
    mapping: List[MappingItem]
    missingInfo: List[str]


class AnalyzeRequest(BaseModel):
    github_url: Optional[str] = None
