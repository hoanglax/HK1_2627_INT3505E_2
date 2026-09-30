from flask import Flask, jsonify, request

app = Flask(__name__)
_next = 2

BOOKS = [{"id": 1, "title": "Clean Code", "author": "R. Martin"}]

def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

# GET - list of books
@app.route("/books", methods=["GET"])
def list_book():
    n = int(request.args.get("limit", 100))
    return jsonify(BOOKS[:n]), 200

# GET - 1 book
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find(bid)
    if book is None:
        return {"error": "not found"}, 404
    return jsonify(book), 200

#CREATE - POST
@app.route("/books", methods=["POST"])
def create_book():
    global _next
    body = request.get_json(silent=True) or {}
    t, a = body.get("title"), body.get("author")
    if not t or not a:
        return {"error": "need title + author"}, 400

    book = {"id": _next, "title": t, "author": a}
    _next += 1
    BOOKS.append(book)
    return jsonify(book), 201, {"Location":f"/books/{book['id']}"}

# UPDATE - PUT
@app.route("/books/<int:bid>", methods=["PUT"])
def modify_book(bid):
    book = find(bid)
    if not book: return {"error": "not found"}, 404
    book.update(request.get_json(silent=True) or {})
    return jsonify(book), 200

# DELETE
@app.route("/books/<int:bid>", methods=["DELETE"])
def delete_book(bid):
    book = find(bid)
    if not book: return {"error": "not found"}, 404
    BOOKS.remove(book)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)