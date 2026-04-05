from typing import Optional

from pydantic import BaseModel


class LiteratureBase(BaseModel):
    title: str
    authors: str
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    keywords: Optional[str] = None
    note: Optional[str] = None
    pdf_path: Optional[str] = None


class LiteratureCreate(LiteratureBase):
    pass


class LiteratureUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    keywords: Optional[str] = None
    note: Optional[str] = None
    pdf_path: Optional[str] = None


class LiteratureOut(LiteratureBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
