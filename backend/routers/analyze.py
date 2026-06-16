import asyncio
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from pypdf.errors import PdfReadError

from component_extractor import extract_components
from mock_data import MOCK_RESULT
from models.schemas import AnalysisResult, Components, PaperInfo
from paper_parser import build_paper_info, parse_pdf

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
    components = Components(**extract_components(parsed))

    # Simulate analysis latency; replace with real LLM call later
    await asyncio.sleep(1.5)

    return MOCK_RESULT.model_copy(update={"paperInfo": paper_info, "components": components})
