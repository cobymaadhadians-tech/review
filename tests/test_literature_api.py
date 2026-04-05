from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_list_literature_with_pdf():
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    files = {"pdf": ("sample.pdf", BytesIO(pdf_content), "application/pdf")}
    data = {
        "title": "Glioma Review",
        "authors": "A. Doctor",
        "year": "2024",
        "journal": "Neurosurgery Journal",
        "doi": "10.1000/test-doi",
        "keywords": "glioma,review",
        "note": "test",
    }

    create_resp = client.post("/api/literatures", data=data, files=files)
    assert create_resp.status_code == 200

    list_resp = client.get("/api/literatures")
    assert list_resp.status_code == 200
    payload = list_resp.json()
    assert len(payload) >= 1
    assert payload[0]["pdf_path"] is not None
    assert payload[0]["pdf_path"].startswith("/data/pdfs/")

    open_pdf_resp = client.get(payload[0]["pdf_path"])
    assert open_pdf_resp.status_code == 200


def test_batch_import_with_filename_parsing():
    pdf_content_1 = b"%PDF-1.4\nDummy one\n%%EOF"
    pdf_content_2 = b"%PDF-1.4\nDummy two\n%%EOF"

    files = [
        ("files", ("2023_Glioma_Clinical_Study.pdf", BytesIO(pdf_content_1), "application/pdf")),
        ("files", ("Mechanism-Paper-2021.pdf", BytesIO(pdf_content_2), "application/pdf")),
    ]

    resp = client.post("/api/literatures/batch-import", files=files)
    assert resp.status_code == 200
    payload = resp.json()

    assert payload["total"] == 2
    assert payload["imported"] == 2
    assert payload["failed"] == 0

    list_resp = client.get("/api/literatures?query=Glioma")
    assert list_resp.status_code == 200
    assert any("Glioma" in item["title"] for item in list_resp.json())
