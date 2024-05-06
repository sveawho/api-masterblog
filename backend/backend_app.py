from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

POSTS_FILE = "posts.json"


def load_posts():
    """Load posts from JSON file."""
    try:
        with open(POSTS_FILE, "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    return posts


def save_posts(posts):
    """Save posts to JSON file."""
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Retrieve all posts."""
    posts = load_posts()
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new post."""
    if not request.json or 'title' not in request.json or not request.json['title'] or 'content' not in request.json or not request.json['content'] or 'author' not in request.json or not request.json['author'] or 'date' not in request.json or not request.json['date']:
        abort(400, 'Missing or empty required fields')

    new_post = {
        "id": len(load_posts()) + 1,
        "title": request.json['title'],
        "content": request.json['content'],
        "author": request.json['author'],
        "date": request.json['date']
    }

    posts = load_posts()
    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID."""
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID."""
    posts = load_posts()
    post = next((post for post in posts if post['id'] == post_id), None)
    if not post:
        abort(404, f"Post with id {post_id} not found")

    data = request.json
    if 'title' in data:
        if not data['title']:
            abort(400, 'Title cannot be empty')
        post['title'] = data['title']
    if 'content' in data:
        if not data['content']:
            abort(400, 'Content cannot be empty')
        post['content'] = data['content']
    if 'author' in data:
        if not data['author']:
            abort(400, 'Author cannot be empty')
        post['author'] = data['author']
    if 'date' in data:
        if not data['date']:
            abort(400, 'Date cannot be empty')
        post['date'] = data['date']

    save_posts(posts)
    return jsonify(post)


@app.route('/api/update/<int:post_id>', methods=['GET', 'POST'])
def get_post(post_id):
    """Render the update page."""
    if request.method == 'GET':
        posts = load_posts()
        post = next((post for post in posts if post['id'] == post_id), None)
        return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search posts based on a query."""
    query = request.args.get('query')

    if not query:
        abort(400, 'Missing search query')

    posts = load_posts()
    search_results = [post for post in posts if
                      query.lower() in post['title'].lower() or query.lower() in post['content'].lower()]
    return jsonify(search_results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
