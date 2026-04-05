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
