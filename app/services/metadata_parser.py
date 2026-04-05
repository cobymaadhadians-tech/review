from __future__ import annotations

import re
from pathlib import Path


_YEAR_REGEX = re.compile(r"\b(19\d{2}|20\d{2}|21\d{2})\b")


def extract_from_filename(filename: str) -> tuple[str, int | None]:
    stem = Path(filename).stem
    cleaned = stem.replace("_", " ").replace("-", " ").strip()
    year_match = _YEAR_REGEX.search(cleaned)
    year = int(year_match.group(1)) if year_match else None
    title = re.sub(r"\s+", " ", cleaned).strip() or "Untitled"
    return title, year


def try_extract_title_from_pdf(file_path: Path) -> str | None:
    """Best-effort PDF title extraction; silently fallback if dependency not installed."""
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    try:
        reader = PdfReader(str(file_path))
        meta_title = getattr(getattr(reader, "metadata", None), "title", None)
        if meta_title and str(meta_title).strip():
            return str(meta_title).strip()

        if reader.pages:
            text = reader.pages[0].extract_text() or ""
            first_line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
            if first_line:
                return first_line[:300]
    except Exception:
        return None

    return None
