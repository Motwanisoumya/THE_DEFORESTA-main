from flask import Flask, request, abort, send_from_directory, jsonify
from flask_cors import CORS
import os
import subprocess
import shutil
import time
app = Flask(__name__)
CORS(app)



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, 'No file part in the request')
    file = request.files['file']
    save_path = os.path.join('./frontend/static/display', file.filename)
    print(f'Saving file to {save_path}')
    file.save(save_path)
    return file.filename

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('./frontend/static/display', filename)

@app.route('/', methods=['GET'])
def get_all_images():
    image_dir = './frontend/static/display'
    images = os.listdir(image_dir)
    return jsonify(images)

@app.route('/run_script', methods=['POST'])
def run_script():
    print("reached here ")
    subprocess.run(['python3', 'amazon.py'])
    #subprocess.run(['python3', 'clear.py'])
    subprocess.run(['python3', 'delete.py'])
    time.sleep(1)
    return 'Script executed'

if __name__ == '__main__':
    app.run(port=5000)