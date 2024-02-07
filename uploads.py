# upload.py
from flask import Blueprint, jsonify, request, render_template, send_from_directory
import os

uploads_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

uploads_bp.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads_bp.route('/upload-files/', methods=['POST'])  # Change this to match the url_prefix specified in main.py
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        file.save(os.path.join(uploads_bp.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"error": "File type not allowed"})


@uploads_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(uploads_bp.config['UPLOAD_FOLDER'], filename, as_attachment=True)
