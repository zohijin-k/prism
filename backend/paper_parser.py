from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

PREVIEW_CHARS = 800


def extract_paper_info(filename: str, content: bytes) -> dict:
    """
    Extract metadata and a text preview from a PDF.
    Returns a dict matching the PaperInfo schema.
    Never raises — on any failure, extraction_error is set instead.
    """
    try:
        reader = PdfReader(BytesIO(content))
        page_count = len(reader.pages)

        chunks: list[str] = []
        total = 0
        for page in reader.pages:
            text = page.extract_text() or ""
            chunks.append(text)
            total += len(text)
            if total >= PREVIEW_CHARS:
                break

        raw = "\n".join(chunks).strip()
        if not raw:
            return {
                "filename": filename,
                "page_count": page_count,
                "text_preview": "(No selectable text found — this PDF may be image-only or scanned.)",
                "extraction_error": None,
            }

        preview = raw[:PREVIEW_CHARS]
        if len(raw) > PREVIEW_CHARS:
            preview = preview.rstrip() + "…"

        return {
            "filename": filename,
            "page_count": page_count,
            "text_preview": preview,
            "extraction_error": None,
        }

    except PdfReadError as exc:
        return {
            "filename": filename,
            "page_count": 0,
            "text_preview": "",
            "extraction_error": f"Could not read PDF: {exc}",
        }
    except Exception as exc:
        return {
            "filename": filename,
            "page_count": 0,
            "text_preview": "",
            "extraction_error": f"Unexpected error during extraction: {exc}",
        }
