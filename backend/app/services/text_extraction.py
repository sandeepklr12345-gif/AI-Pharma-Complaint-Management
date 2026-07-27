from io import BytesIO
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def extract_text_from_plain(file_bytes: bytes) -> str:
    """For .txt / .eml style email exports — just decode."""
    return file_bytes.decode("utf-8", errors="ignore").strip()


def extract_text(filename: str, file_bytes: bytes) -> tuple[str, str]:
    """
    Returns (extracted_text, file_type).
    Production-grade OCR isn't required by the assignment, so images
    aren't handled here — paste the complaint text directly for those.
    """
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes), "pdf"
    if lower.endswith((".txt", ".eml")):
        return extract_text_from_plain(file_bytes), "email"
    raise ValueError(f"Unsupported file type for: {filename}")
