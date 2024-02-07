from flask import Flask, render_template, Blueprint, request, jsonify, send_from_directory
from users import users_bp
from orders import orders_bp
# from uploads import uploads_bp
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Flask App', welcome_message='Welcome to the....',
                           content='Home Page.')


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({"message": "File uploaded successfully"})

    return jsonify({"error": "File type not allowed"})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Register users_bp and orders_bp with the app
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
# app.register_blueprint(uploads_bp, url_prefix='/api/upload')

if __name__ == "__main__":
    app.run(debug=True)
