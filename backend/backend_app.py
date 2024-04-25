from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

POSTS_FILE = "posts.json"


def load_posts():
    """
    Load posts from a JSON file.

    Tries to open the file specified by POSTS_FILE for reading.
    If the file exists, it reads its contents using json.load().
    If the file doesn't exist, it returns an empty list.
    """
    try:
        with open(POSTS_FILE, "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    return posts


def save_posts(posts):
    """
    Save posts to a JSON file.

    Writes the contents of the posts list to the file specified by POSTS_FILE
    using json.dump() with an indentation level of 4.
    """
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    GET endpoint to retrieve all posts.

    Loads the posts from the JSON file using load_posts(),
    and returns them as a JSON response using jsonify().
    """
    posts = load_posts()
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    POST endpoint to add a new post.

    Checks if the request contains JSON data and if all required fields
    ('title', 'content', 'author', 'date') are present.
    If so, it creates a new post dictionary with an ID incremented by one
    from the length of the current posts. It then appends the new post to
    the list of posts, saves it using save_posts(), and returns the new post
    as a JSON response.
    """
    if not request.json or not all(key in request.json for key in ['title', 'content', 'author', 'date']):
        abort(400, 'Missing required fields')

    new_post = {
        "id": len(load_posts()) + 1,
        **{key: request.json[key] for key in ['title', 'content', 'author', 'date']}
    }

    posts = load_posts()
    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    DELETE endpoint to delete a post.

    Deletes the post with the specified post_id from the list of posts,
    saves the updated list using save_posts(), and returns a JSON response
    indicating that the post has been deleted successfully.
    """
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
