from fastapi import FastAPI
from fastapi.responses import JSONResponse
from PIL import Image
from PyPDF2 import PdfReader
import base64
import uuid
import tempfile
import shutil
import pdfkit
import pypdfium2 as pdfium
from io import BytesIO
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/")
async def check_api():
    return "Welcome, this is working"

@app.get("/check_dependencies")
async def check_dependencies():
    result = {}

    try:
        class Item(BaseModel):
            name: str
            quantity: int
            description: Optional[str] = None
        Item(name="Test", quantity=5)
        result["pydantic"] = "✅ working"
    except Exception as e:
        result["pydantic"] = f"❌ {str(e)}"

    try:
        html = "<h1>Hello PDF</h1>"
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            pdfkit.from_string(html, f.name)
            result["pdfkit"] = "✅ working"
    except Exception as e:
        result["pdfkit"] = f"❌ {str(e)}"

    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4\n%Test\n1 0 obj\n<<>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<>>\nstartxref\n0\n%%EOF")
            f.flush()
            pdf = pdfium.PdfDocument(f.name)
            image = pdf[0].render().to_pil()
            if isinstance(image, Image.Image):
                result["pypdfium2"] = "✅ working"
    except Exception as e:
        result["pypdfium2"] = f"❌ {str(e)}"

    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4\n%Test\n1 0 obj\n<<>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<>>\nstartxref\n0\n%%EOF")
            f.flush()
            reader = PdfReader(f.name)
            result["PyPDF2"] = "✅ working"
    except Exception as e:
        result["PyPDF2"] = f"❌ {str(e)}"

    try:
        img = Image.new("RGB", (100, 100), color="red")
        buf = BytesIO()
        img.save(buf, format="PNG")
        result["Pillow"] = "✅ working"
    except Exception as e:
        result["Pillow"] = f"❌ {str(e)}"

    try:
        encoded = base64.b64encode(b"hello").decode()
        decoded = base64.b64decode(encoded).decode()
        assert decoded == "hello"
        _ = str(uuid.uuid4())
        _ = tempfile.TemporaryDirectory()
        result["base64/uuid/tempfile"] = "✅ working"
    except Exception as e:
        result["base64/uuid/tempfile"] = f"❌ {str(e)}"

    return JSONResponse(content=result)
