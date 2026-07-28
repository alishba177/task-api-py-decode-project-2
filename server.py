from flask import Flask, jsonify

from routes.tasks import tasks_bp

app = Flask(__name__)

# Don't force redirects between "/tasks" and "/tasks/" — keep behavior simple and predictable.
app.url_map.strict_slashes = False


@app.get("/")
def root():
    return jsonify({
        "message": "DecodeLabs Task API is running.",
        "endpoints": {
            "GET /tasks": "List all tasks",
            "GET /tasks/:id": "Get a single task",
            "POST /tasks": "Create a new task (JSON body: { title, completed? })"
        }
    }), 200


app.register_blueprint(tasks_bp)


# 404 for anything unmatched, then a general error handler — matching the
# "Critical Vocabulary" status codes from the training slides.
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not Found",
        "message": "The requested route does not exist."
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong on the server."
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
