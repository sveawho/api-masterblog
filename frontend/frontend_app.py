from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/update/<int:post_id>', methods=['GET'])
def update(post_id):
    return render_template("update.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
