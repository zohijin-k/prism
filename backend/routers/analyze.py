import asyncio
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from models.schemas import AnalysisResult
from mock_data import MOCK_RESULT

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_paper(
    paper: UploadFile = File(..., description="Research paper PDF"),
    github_url: Optional[str] = Form(None, description="GitHub repository URL"),
    code_zip: Optional[UploadFile] = File(None, description="Source code ZIP"),
):
    # Simulate analysis latency; replace with real LLM call later
    await asyncio.sleep(1.5)
    return MOCK_RESULT
