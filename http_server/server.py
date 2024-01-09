from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import shutil
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload/<session_id>', methods=['POST'])
def upload_files(session_id):
    files = request.files.getlist('file')

    if not files:
        return jsonify({"error": "No files provided"})

    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_folder, exist_ok=True)

    uploaded_files = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(session_folder, filename))
            uploaded_files.append(filename)
        else:
            return jsonify({"error": "Invalid file type"})

    return jsonify({"success": "Files uploaded successfully", "uploaded_files": uploaded_files})


@app.route('/delete_files/<session_id>', methods=['DELETE'])
def delete(session_id):
    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    zip_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.zip")

    try:
        shutil.rmtree(session_folder)
        os.remove(zip_file)
        return jsonify({"success": f"Session {session_id} files deleted successfully"})
    except FileNotFoundError:
        return jsonify({"error": f"Session {session_id} not found"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/download_zip/<session_id>', methods=['GET'])
def download_zip(session_id):
    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)

    if not os.path.exists(session_folder):
        return jsonify({"error": f"No files found for session ID: {session_id}"})

    filename = shutil.make_archive(os.path.join(
        app.config['UPLOAD_FOLDER'], session_id), 'zip', session_folder)
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
