import os
import base64
import uuid
import tempfile
import shutil

from io import BytesIO
from PIL import Image

from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional

import pdfkit
import pypdfium2 as pdfium
from PyPDF2 import PdfReader

def test_fastapi_components():
    print("✅ FastAPI basic setup test:")
    app = FastAPI()
    router = APIRouter()

    @router.get("/ping")
    async def ping():
        return {"message": "pong"}

    app.include_router(router)
    print("  → FastAPI + APIRouter working.")

def test_pydantic():
    print("✅ Pydantic test:")
    class Item(BaseModel):
        name: str
        quantity: int
        description: Optional[str] = None

    item = Item(name="Test", quantity=5)
    assert item.name == "Test"
    print("  → Pydantic BaseModel working.")

def test_pdfkit():
    print("✅ PDFKit test:")
    html = "<h1>Hello PDF</h1>"
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        pdfkit.from_string(html, f.name)
        assert os.path.exists(f.name)
    print("  → pdfkit generated a PDF file successfully.")

def test_pypdfium2():
    print("✅ PyPDFium2 test:")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(b"%PDF-1.4\n%Test\n1 0 obj\n<<>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<>>\nstartxref\n0\n%%EOF")
        f.flush()
        pdf = pdfium.PdfDocument(f.name)
        image = pdf[0].render().to_pil()
        assert isinstance(image, Image.Image)
    print("  → pypdfium2 loaded and rendered PDF page.")

def test_pypdf2():
    print("✅ PyPDF2 test:")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(b"%PDF-1.4\n%Test\n1 0 obj\n<<>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<>>\nstartxref\n0\n%%EOF")
        f.flush()
        reader = PdfReader(f.name)
        assert isinstance(reader.pages, list)
    print("  → PyPDF2 loaded PDF file.")

def test_pillow():
    print("✅ Pillow test:")
    img = Image.new("RGB", (100, 100), color="blue")
    buf = BytesIO()
    img.save(buf, format="PNG")
    assert buf.getvalue() != b""
    print("  → Pillow created and saved an image.")

def test_base64_uuid_tempfile():
    print("✅ Other Python core module tests:")
    s = base64.b64encode(b"hello").decode()
    assert base64.b64decode(s).decode() == "hello"

    u = str(uuid.uuid4())
    assert isinstance(u, str)

    with tempfile.TemporaryDirectory() as temp_dir:
        assert os.path.exists(temp_dir)

    print("  → base64, uuid, tempfile all working.")

if __name__ == "__main__":
    print("==== CHECKING DEPENDENCIES ====")
    test_fastapi_components()
    test_pydantic()
    test_pdfkit()
    test_pypdfium2()
    test_pypdf2()
    test_pillow()
    test_base64_uuid_tempfile()
    print("✅ All checks passed.")
