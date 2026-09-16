from urllib.parse import urlencode
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Clean Architecture", "author": "Robert C. Martin"},
    {"id": 3, "title": "1984", "author": "George Orwell"},
    {"id": 4, "title": "Animal Farm", "author": "George Orwell"},
    {"id": 5, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
] # Genarate by AI

_next_id = 1
DEFAULT_SIZE, MAX_SIZE = 20, 100


# 1. GET /books: Lấy danh sách (Có phân trang & Tìm kiếm)
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400

    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    flt = BOOKS
    a = request.args.get("author")
    if a:
        flt = [
            b
            for b in flt
            if b.get("author") and b["author"].lower() == a.lower()
        ]

    q = (request.args.get("q") or "").lower()
    if q:
        flt = [b for b in flt if b.get("title") and q in b["title"].lower()]

    total = len(flt)
    start = (page - 1) * size
    end = start + size

    items = flt[start:end]
    last = max((total + size - 1) // size, 1)

    def u(p):
        args = request.args.copy()
        args["page"] = p
        args["size"] = size
        return f"/books?{urlencode(args)}"

    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(last)},
    }

    if page > 1:
        links["prev"] = {"href": u(page - 1)}
    if end < total:
        links["next"] = {"href": u(page + 1)}

    body = {
        "data": items,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_page": last,
        },
        "_links": links,
    }

    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp


# 2. POST /books: Tạo sách mới
@app.post("/books")
def create_book():
    global _next_id
    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()

    if not t or not a:
        return jsonify(error="title and author required"), 422

    book = {"id": _next_id, "title": t, "author": a}
    BOOKS.append(book)
    _next_id += 1

    resp = make_response(jsonify(book), 201)
    resp.headers["Location"] = f"/books/{book['id']}"
    return resp


# 3. GET /books/<id>: Xem chi tiết 1 cuốn sách
@app.get("/books/<int:bid>")
def fetch(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404

    resp = make_response(jsonify(BOOKS[i]), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp


# 4. PUT /books/<id>: Cập nhật toàn bộ sách
@app.put("/books/<int:bid>")
def put(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404

    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    p = request.get_json(silent=True) or {}
    t = str(p.get("title") or "").strip()
    a = str(p.get("author") or "").strip()

    if not t or not a:
        return jsonify(error="need title + author"), 422

    BOOKS[i] = {
        "id": bid,
        "title": t,
        "author": a,
        "isbn": p.get("isbn"),
        "price": p.get("price"),
    }
    return jsonify(BOOKS[i]), 200


# 5. PATCH /books/<id>: Sửa từng trường của sách
@app.patch("/books/<int:bid>")
def patch(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404

    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    p = request.get_json(silent=True) or {}

    if "price" in p:
        price = p["price"]
        if not isinstance(price, (int, float)) or price < 0:
            return jsonify(error="price must be a positive number"), 422

    for k in "title author isbn price".split():
        if k in p:
            val = p[k]
            BOOKS[i][k] = val.strip() if isinstance(val, str) else val

    return jsonify(BOOKS[i]), 200


# 6. DELETE /books/<id>: Xóa sách
@app.delete("/books/<int:bid>")
def delete(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None:
        return jsonify(error="not found"), 404

    BOOKS.pop(i)
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)