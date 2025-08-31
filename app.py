from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='frontend/build')
CORS(app)

STORAGE_DIR = "storage"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = []
    for filename in os.listdir(STORAGE_DIR):
        if filename.endswith((".md", ".txt")):
            notes.append(filename)
    return jsonify(notes)

@app.route('/api/notes/<filename>', methods=['GET'])
def get_note(filename):
    file_path = os.path.join(STORAGE_DIR, filename)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"content": content})
    except IOError as e:
        return jsonify({"error": f"Could not load note: {e}"}), 404

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    content = data.get('content', '')
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    first_line = content.split('\n')[0][:50].strip()
    if not first_line:
        first_line = "Untitled"

    base_filename = "".join(c for c in first_line if c.isalnum() or c in (' ', '-', '_')).strip()
    if not base_filename:
        base_filename = "Untitled"

    filename = f"{base_filename}.md"
    file_path = os.path.join(STORAGE_DIR, filename)

    i = 1
    while os.path.exists(file_path):
        filename = f"{base_filename} ({i}).md"
        file_path = os.path.join(STORAGE_DIR, filename)
        i += 1

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return jsonify({"filename": filename}), 201
    except IOError as e:
        return jsonify({"error": f"Could not save note: {e}"}), 500

@app.route('/api/notes/<filename>', methods=['DELETE'])
def delete_note(filename):
    file_path = os.path.join(STORAGE_DIR, filename)
    try:
        os.remove(file_path)
        return jsonify({}), 204
    except OSError as e:
        return jsonify({"error": f"Could not delete note: {e}"}), 500

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)
