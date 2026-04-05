from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import BASE_DIR, PDF_DIR
from app.schemas import LiteratureCreate, LiteratureUpdate
from app.services.literature_service import (
    create_literature,
    delete_literature,
    get_literature,
    list_literatures,
    update_literature,
)
from app.services.metadata_parser import extract_from_filename, try_extract_title_from_pdf

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


def _resolve_local_path(web_path: str) -> Path:
    return BASE_DIR / web_path.lstrip("/")


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


@router.post("/batch-import")
def api_batch_import_literatures(
    files: list[UploadFile] = File(...),
    doi: str | None = Form(default=None),
):
    results: list[dict[str, str | int | None]] = []

    for upload in files:
        entry: dict[str, str | int | None] = {
            "filename": upload.filename,
            "status": "skipped",
            "id": None,
            "error": None,
        }

        try:
            if not upload.filename or not upload.filename.lower().endswith(".pdf"):
                entry["error"] = "Only PDF files are supported"
                results.append(entry)
                continue

            pdf_path = _save_pdf(upload)
            if not pdf_path:
                entry["error"] = "Failed to save PDF"
                results.append(entry)
                continue

            local_path = _resolve_local_path(pdf_path)
            title_from_name, inferred_year = extract_from_filename(upload.filename)
            parsed_title = try_extract_title_from_pdf(local_path)
            title = parsed_title or title_from_name

            payload = LiteratureCreate(
                title=title,
                authors="",
                year=inferred_year,
                journal=None,
                doi=doi,
                keywords=None,
                note="auto-imported",
                pdf_path=pdf_path,
            )
            lit_id = create_literature(payload)
            entry["status"] = "imported"
            entry["id"] = lit_id
        except Exception as exc:  # keep batch processing alive per file
            entry["error"] = str(exc)

        results.append(entry)

    imported = sum(1 for r in results if r["status"] == "imported")
    return {
        "total": len(results),
        "imported": imported,
        "failed": len(results) - imported,
        "results": results,
    }


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
        local_pdf = _resolve_local_path(item["pdf_path"])
        if local_pdf.exists() and local_pdf.is_file():
            local_pdf.unlink()

    ok = delete_literature(lit_id)
    return {"ok": ok}
