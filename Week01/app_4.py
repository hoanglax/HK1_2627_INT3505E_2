from flask import Flask, jsonify

app = Flask(__name__)

BOOKS = [
    {"id": "abc-123", "t": "python"},
    {"id": "def456", "t": "Java"}
]

def find_by_id(book_id):
    return next((b for b in BOOKS if b["id"] == book_id), None)

#Path param

# /book/<id> - id là string
@app.route("/book/<book_id>", methods=["GET"])
def get_book(book_id):
    book = find_by_id(book_id)

    if book is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200

# Ép kiểu int ngay từ URL
@app.route("/items/<int:item_id>")
def get_item(item_id):
    return jsonify({"id": item_id}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)