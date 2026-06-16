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
    matchedSentence: Optional[str] = None
    score: Optional[int] = None


class MetricsField(BaseModel):
    value: List[str]
    source: Optional[str] = None
    confidence: Literal["High", "Medium", "Low"]
    found: bool
    matchedSentence: Optional[str] = None
    score: Optional[int] = None


class HyperparametersField(BaseModel):
    value: Dict[str, str]
    source: Optional[str] = None
    confidence: Literal["High", "Medium", "Low"]
    found: bool
    matchedSentence: Optional[str] = None
    score: Optional[int] = None


class Components(BaseModel):
    dataset: ComponentField
    model: ComponentField
    backbone: ComponentField
    loss: ComponentField
    optimizer: ComponentField
    metrics: MetricsField
    hyperparameters: HyperparametersField


class CodeHints(BaseModel):
    models: List[str]
    backbones: List[str]
    losses: List[str]
    optimizers: List[str]
    datasets: List[str]
    metrics: List[str]
    config: Dict[str, str]


class RepoAnalysis(BaseModel):
    inputType: Literal["github", "zip", "none"]
    repoName: Optional[str] = None
    status: str
    relevantFiles: List[str]
    fileCount: int
    codeHints: CodeHints


class ComparisonItem(BaseModel):
    item: str
    paper: str
    code: str
    status: Literal["Match", "Partial Match", "Mismatch", "Paper Only", "Code Only", "Unknown"]
    confidence: Literal["High", "Medium", "Low"]
    explanation: str


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
    repoAnalysis: RepoAnalysis
    comparison: List[ComparisonItem]
    mapping: List[MappingItem]
    missingInfo: List[str]
