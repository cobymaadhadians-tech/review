import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import PDF_DIR
from app.schemas import LiteratureCreate, LiteratureUpdate
from app.services.literature_service import (
    create_literature,
    delete_literature,
    get_literature,
    list_literatures,
    update_literature,
)

router = APIRouter(prefix="/api/literatures", tags=["literatures"])


def _save_pdf(pdf: UploadFile | None) -> str | None:
    if pdf is None or not pdf.filename:
        return None

    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    suffix = Path(pdf.filename).suffix
    filename = f"{uuid.uuid4().hex}{suffix}"
    target = PDF_DIR / filename

    with target.open("wb") as f:
        shutil.copyfileobj(pdf.file, f)

    return f"/data/pdfs/{filename}"


@router.get("")
def api_list_literatures(query: str | None = None):
    return list_literatures(query=query)


@router.get("/{lit_id}")
def api_get_literature(lit_id: int):
    item = get_literature(lit_id)
    if not item:
        raise HTTPException(status_code=404, detail="Literature not found")
    return item


@router.post("")
def api_create_literature(
    title: str = Form(...),
    authors: str = Form(...),
    year: int | None = Form(default=None),
    journal: str | None = Form(default=None),
    doi: str | None = Form(default=None),
    keywords: str | None = Form(default=None),
    note: str | None = Form(default=None),
    pdf: UploadFile | None = File(default=None),
):
    pdf_path = _save_pdf(pdf)
    payload = LiteratureCreate(
        title=title,
        authors=authors,
        year=year,
        journal=journal,
        doi=doi,
        keywords=keywords,
        note=note,
        pdf_path=pdf_path,
    )
    lit_id = create_literature(payload)
    return {"id": lit_id}


@router.put("/{lit_id}")
def api_update_literature(lit_id: int, payload: LiteratureUpdate):
    ok = update_literature(lit_id, payload)
    if not ok:
        raise HTTPException(status_code=404, detail="Literature not found or no fields to update")
    return {"ok": True}


@router.delete("/{lit_id}")
def api_delete_literature(lit_id: int):
    item = get_literature(lit_id)
    if not item:
        raise HTTPException(status_code=404, detail="Literature not found")

    if item.get("pdf_path"):
        local_pdf = Path(item["pdf_path"].lstrip("/"))
        if local_pdf.exists() and local_pdf.is_file():
            local_pdf.unlink()

    ok = delete_literature(lit_id)
    return {"ok": ok}
