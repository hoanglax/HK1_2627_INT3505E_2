"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""

import pytest
from tools import get_book_schema
from jsonschema import ValidationError, validate


def test_get_books_empty(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.get_json() ==[]

def test_get_invalid_books(client):
    response = client.get("/books/9999")

    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"

def test_post_books_with_only_author(client):
    response = client.post("/books", json={"author": "HOANG"})

    assert response.status_code == 400 
    body = response.get_json()
    fields = [error["field"] for error in body ["errors"]]

    assert "title" in fields

def test_delete_then_get_404(client):
    response = client.post(
        "/books",
        json={
            "title": "Python",
            "author": "Hoang"
        }
    )

    assert response.status_code == 201

    book_id = response.get_json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 404



def test_response_extra_field_blocked(client, sample_book):
    book_schema = get_book_schema()

    for field_schema in book_schema.get("properties", {}).values():
        if field_schema.get("nullable") is True:
            original_type = field_schema["type"]
            field_schema["type"] = [original_type, "null"]
            field_schema.pop("nullable", None)

    response = client.get(f"/books/{sample_book}")
    assert response.status_code == 200

    book = response.get_json()
    validate(instance=book, schema=book_schema)

    modified_book = book.copy()
    modified_book["password_hash"] = "secret123"

    with pytest.raises(ValidationError):
        validate(instance=modified_book, schema=book_schema)
