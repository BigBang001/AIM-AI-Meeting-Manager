from flask import Flask, send_from_directory, request, jsonify
from assistant.core import ContextManager
import os

app = Flask(__name__)
WEB_UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ui")
context = ContextManager(max_tokens=50)

def serialize_entry(e):
    return {
        "prompt": e['prompt'],
        "responses": e['responses'],
        "finalized": e['finalized'],
        "pinned": e['pinned'],
        "timestamp": e['timestamp'].isoformat()
    }

def segregate_memory():
    active, finalized, pinned = [], [], []
    for e in context.show_history():
        if e['pinned']:
            pinned.append(e)
        elif e['finalized']:
            finalized.append(e)
        elif len(e['responses']) > 0:
            active.append(e)
    return active, finalized, pinned

@app.route("/")
def index():
    return send_from_directory(WEB_UI_PATH, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(WEB_UI_PATH, path)

@app.route("/add_prompt", methods=["POST"])
def add_prompt():
    prompt = request.json.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error":"Prompt cannot be empty!"}), 400
    success, resp_or_error = context.add_prompt(prompt)
    if not success:
        return jsonify({"error": resp_or_error}), 400
    active, finalized, pinned = segregate_memory()
    return jsonify({
        "active":[serialize_entry(e) for e in active],
        "finalized":[serialize_entry(e) for e in finalized],
        "pinned":[serialize_entry(e) for e in pinned],
        "memory_bar": context.show_memory_bar()
    })

@app.route("/undo", methods=["POST"])
def undo():
    resp = context.undo_response()
    active, finalized, pinned = segregate_memory()
    return jsonify({
        "active":[serialize_entry(e) for e in active],
        "finalized":[serialize_entry(e) for e in finalized],
        "pinned":[serialize_entry(e) for e in pinned],
        "memory_bar": context.show_memory_bar(),
        "warning": None if resp else "No responses to undo!"
    })

@app.route("/finalize", methods=["POST"])
def finalize():
    success = context.finalize_prompt()
    active, finalized, pinned = segregate_memory()
    return jsonify({
        "active":[serialize_entry(e) for e in active],
        "finalized":[serialize_entry(e) for e in finalized],
        "pinned":[serialize_entry(e) for e in pinned],
        "memory_bar": context.show_memory_bar(),
        "message":"Prompt finalized!" if success else "Nothing to finalize."
    })

@app.route("/pin", methods=["POST"])
def pin():
    index = int(request.json.get("index", -1))
    context.pin_prompt(index)
    active, finalized, pinned = segregate_memory()
    return jsonify({
        "active":[serialize_entry(e) for e in active],
        "finalized":[serialize_entry(e) for e in finalized],
        "pinned":[serialize_entry(e) for e in pinned],
        "memory_bar": context.show_memory_bar()
    })

if __name__=="__main__":
    app.run(debug=True)
