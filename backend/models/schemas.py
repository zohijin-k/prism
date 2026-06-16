from pydantic import BaseModel
from typing import Dict, List, Literal, Optional


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


class ComponentField(BaseModel):
    value: str
    source: Optional[str] = None
    confidence: Literal["High", "Medium", "Low"]
    found: bool


class MetricsField(BaseModel):
    value: List[str]
    source: Optional[str] = None
    confidence: Literal["High", "Medium", "Low"]
    found: bool


class HyperparametersField(BaseModel):
    value: Dict[str, str]
    source: Optional[str] = None
    confidence: Literal["High", "Medium", "Low"]
    found: bool


class Components(BaseModel):
    dataset: ComponentField
    model: ComponentField
    backbone: ComponentField
    loss: ComponentField
    optimizer: ComponentField
    metrics: MetricsField
    hyperparameters: HyperparametersField


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
