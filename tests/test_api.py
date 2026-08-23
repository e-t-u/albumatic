from fastapi.testclient import TestClient
from albumatic.api import app

client = TestClient(app)


def test_get_sizes():
    response = client.get("/api/v1/sizes")
    assert response.status_code == 200
    data = response.json()
    assert "A" in data
    assert data["A"]["width_mm"] == 20.0
    assert data["A"]["height_mm"] == 24.0
    assert data["A"]["width_in"] == 0.79
    assert data["A"]["height_in"] == 0.94
    assert "a" in data
    assert data["a"]["orientation"] == "landscape"


def test_render_pdf_post():
    payload = {
        "country": "France",
        "area": "Bordeaux",
        "year": "1870",
        "no": "1",
        "template": "AA-BB",
    }
    response = client.post("/api/v1/render/pdf", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_render_album_pdf_post():
    payload = {
        "country": "Nepal",
        "pages": [
            {"template": "XXX-XXX", "no": "1", "area": "Page 1", "year": "1881"},
            {"template": "dd-dd", "no": "2", "area": "Page 2", "year": "1907"},
            {"template": "AAAA-EEEE", "no": "3", "area": "Page 3", "year": "1954"},
        ]
    }
    response = client.post("/api/v1/render/album/pdf", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_batch_parse_and_serialize():
    parse_payload = {
        "text": "AA-BB-CC\ncc-ddd-a\nXXXX",
        "country": "USA",
        "year": "2009"
    }
    response = client.post("/api/v1/batch/parse", json=parse_payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["pages"]) == 3
    assert data["pages"][0]["template"] == "AA-BB-CC"

    # Serialize
    serialize_payload = data["pages"]
    response2 = client.post("/api/v1/batch/serialize", json=serialize_payload)
    assert response2.status_code == 200
    assert "AA-BB-CC" in response2.json()["text"]


def test_render_svg_post():
    payload = {
        "country": "Sweden",
        "area": "Skilling",
        "year": "1855",
        "no": "1",
        "template": "A-B",
    }
    response = client.post("/api/v1/render/svg", json=payload)
    assert response.status_code == 200
    assert "image/svg+xml" in response.headers["content-type"]
    assert "<svg" in response.text


def test_legacy_pdf_endpoint():
    response = client.get("/pdf/USA/Definitives/2009/1/ABBA-hh-BBB/1.pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_gui_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Albumatic" in response.text
