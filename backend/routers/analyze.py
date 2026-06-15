import asyncio
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from models.schemas import AnalysisResult, PaperInfo
from mock_data import MOCK_RESULT
from paper_parser import extract_paper_info

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_paper(
    paper: UploadFile = File(..., description="Research paper PDF"),
    github_url: Optional[str] = Form(None, description="GitHub repository URL"),
    code_zip: Optional[UploadFile] = File(None, description="Source code ZIP"),
):
    content = await paper.read()
    info_dict = extract_paper_info(paper.filename or "unknown.pdf", content)
    paper_info = PaperInfo(**info_dict)

    # Simulate analysis latency; replace with real LLM call later
    await asyncio.sleep(1.5)

    return MOCK_RESULT.model_copy(update={"paperInfo": paper_info})
