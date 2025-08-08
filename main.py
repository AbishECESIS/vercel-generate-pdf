from fastapi import FastAPI
from fastapi.responses import JSONResponse
from PIL import Image
from PyPDF2 import PdfReader
import base64
import uuid
import tempfile
from io import BytesIO
from pydantic import BaseModel
from typing import Optional
from weasyprint import HTML
from reportlab.pdfgen import canvas

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

    # ✅ WeasyPrint test
    try:
        html = "<h1>Hello from WeasyPrint</h1><p>This is a PDF!</p>"
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            HTML(string=html).write_pdf(f.name)
            result["weasyprint"] = "✅ working"
    except Exception as e:
        result["weasyprint"] = f"❌ {str(e)}"
        

    try:
        from PyPDF2 import PdfWriter, PdfReader

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            writer = PdfWriter()
            writer.add_blank_page(width=100, height=100)
            writer.write(f)
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
