"""File text extraction and the /api/upload endpoint."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers import upload
from app.services.text_extraction import extract_text


def make_pdf(text: str) -> bytes:
    """Smallest valid one-page PDF containing `text` (avoids a PDF-writing dependency)."""
    stream = f"BT /F1 12 Tf 20 100 Td ({text}) Tj ET".encode()
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF" % (len(objs) + 1, xref)
    return out


# ---------- extract_text ----------

def test_txt_and_eml_are_decoded_as_email():
    assert extract_text("c.txt", b"  Tablet is crumbling  ") == ("Tablet is crumbling", "email")
    assert extract_text("MAIL.EML", "café".encode()) == ("café", "email")


def test_pdf_text_is_extracted():
    text, kind = extract_text("report.pdf", make_pdf("Batch B-17 failed dissolution"))
    assert kind == "pdf"
    assert "Batch B-17 failed dissolution" in text


def test_unsupported_extension_is_rejected():
    with pytest.raises(ValueError, match="Unsupported"):
        extract_text("scan.png", b"\x89PNG")


# ---------- endpoint ----------

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(upload.router)
    return TestClient(app)


def test_upload_returns_text(client):
    r = client.post("/api/upload", files={"file": ("c.txt", b"Wrong strength on label", "text/plain")})
    assert r.status_code == 200
    assert r.json() == {"text": "Wrong strength on label", "file_type": "email"}


def test_upload_unsupported_type_is_400(client):
    r = client.post("/api/upload", files={"file": ("c.docx", b"x", "application/octet-stream")})
    assert r.status_code == 400


def test_upload_empty_file_is_422(client):
    r = client.post("/api/upload", files={"file": ("c.txt", b"   ", "text/plain")})
    assert r.status_code == 422
