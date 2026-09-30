from flask import Flask, jsonify, request

app = Flask(__name__)

posts_db = [
    {"id": 1, "title": "Bài viết đầu tiên", "content": "Nội dung...", "author_id": 101},
    {"id": 2, "title": "Học RESTful API", "content": "Nội dung...", "author_id": 102}
]

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    return jsonify({
        "status": "success",
        "data": posts_db,
        "page": page,
        "limit": limit
    }), 200

@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Thiếu dữ liệu tiêu đề hoặc nội dung"}), 400
        
    new_post = {
        "id": len(posts_db) + 1,
        "title": data['title'],
        "content": data['content'],
        "author_id": data.get('author_id', 1)
    }
    
    posts_db.append(new_post)
    
    return jsonify({
        "status": "success",
        "data": new_post
    }), 201

if __name__ == '__main__':
    app.run(debug=True)