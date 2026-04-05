from typing import Any

from app.db import get_conn
from app.schemas import LiteratureCreate, LiteratureUpdate


ALLOWED_COLUMNS = {"title", "authors", "year", "journal", "doi", "keywords", "note", "pdf_path"}


def create_literature(payload: LiteratureCreate) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO literatures (title, authors, year, journal, doi, keywords, note, pdf_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.title,
                payload.authors,
                payload.year,
                payload.journal,
                payload.doi,
                payload.keywords,
                payload.note,
                payload.pdf_path,
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_literatures(query: str | None = None) -> list[dict[str, Any]]:
    with get_conn() as conn:
        if query:
            like = f"%{query}%"
            rows = conn.execute(
                """
                SELECT * FROM literatures
                WHERE title LIKE ? OR authors LIKE ? OR keywords LIKE ? OR doi LIKE ?
                ORDER BY year DESC, id DESC
                """,
                (like, like, like, like),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM literatures ORDER BY year DESC, id DESC"
            ).fetchall()

    return [dict(row) for row in rows]


def get_literature(lit_id: int) -> dict[str, Any] | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM literatures WHERE id = ?", (lit_id,)).fetchone()
    return dict(row) if row else None


def update_literature(lit_id: int, payload: LiteratureUpdate) -> bool:
    data = payload.model_dump(exclude_unset=True)
    fields = [k for k in data if k in ALLOWED_COLUMNS]
    if not fields:
        return False

    set_clause = ", ".join(f"{field} = ?" for field in fields)
    values = [data[field] for field in fields]
    values.append(lit_id)

    with get_conn() as conn:
        cur = conn.execute(f"UPDATE literatures SET {set_clause} WHERE id = ?", values)
        conn.commit()
        return cur.rowcount > 0


def delete_literature(lit_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM literatures WHERE id = ?", (lit_id,))
        conn.commit()
        return cur.rowcount > 0
