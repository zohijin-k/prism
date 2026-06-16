import asyncio
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from pypdf.errors import PdfReadError

from comparison_engine import compare_paper_and_code
from component_extractor import extract_components
from gap_engine import detect_gaps
from mapping_engine import build_mappings
from models.schemas import (
    AnalysisResult,
    Components,
    ComparisonItem,
    MappingItem,
    PaperInfo,
    PaperSummary,
    RepoAnalysis,
)
from paper_parser import build_paper_info, parse_pdf
from plan_engine import generate_plan
from repo_analyzer import analyze_repo
from summary_engine import generate_summary

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_paper(
    paper: UploadFile = File(..., description="Research paper PDF"),
    github_url: Optional[str] = Form(None, description="GitHub repository URL"),
    code_zip: Optional[UploadFile] = File(None, description="Source code ZIP"),
):
    content = await paper.read()
    filename = paper.filename or "unknown.pdf"

    parsed: Optional[dict] = None
    error: Optional[str] = None
    try:
        parsed = parse_pdf(content)
    except PdfReadError as exc:
        error = f"Could not read PDF: {exc}"
    except Exception as exc:
        error = f"Unexpected error during extraction: {exc}"

    paper_info = PaperInfo(**build_paper_info(filename, parsed, error))
    components_dict = extract_components(parsed)
    components = Components(**components_dict)

    zip_content = await code_zip.read() if code_zip else None
    repo_dict = analyze_repo(github_url, zip_content)
    repo_analysis = RepoAnalysis(**repo_dict)

    comparison = [
        ComparisonItem(**item) for item in compare_paper_and_code(components_dict, repo_dict["codeHints"])
    ]

    paper_sections = parsed["sections"] if parsed else {}
    full_text = parsed["full_text"] if parsed else ""
    mapping = [
        MappingItem(**item)
        for item in build_mappings(paper_sections, repo_dict["codeHints"], repo_dict["relevantFiles"])
    ]

    summary = PaperSummary(**generate_summary(paper_sections, components_dict, full_text))
    implementation_plan = generate_plan(components_dict)
    missing_info = detect_gaps(full_text, components_dict)

    # Simulate analysis latency; replace with real LLM call later
    await asyncio.sleep(1.5)

    return AnalysisResult(
        paperInfo=paper_info,
        summary=summary,
        implementationPlan=implementation_plan,
        components=components,
        repoAnalysis=repo_analysis,
        comparison=comparison,
        mapping=mapping,
        missingInfo=missing_info,
    )
