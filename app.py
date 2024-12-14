from flask import Flask, render_template, send_file, make_response
import os
import mimetypes
from werkzeug.utils import safe_join
from datetime import datetime
import argparse

# Parse the base directory from command-line arguments
parser = argparse.ArgumentParser(description="Run an image gallery server.")
parser.add_argument(
    '--base_dir', 
    type=str, 
    required=True, 
    help="Base directory where images are stored"
)
args = parser.parse_args()

# Set the base directory where images are stored
BASE_DIR = args.base_dir
if not os.path.exists(BASE_DIR):
    raise FileNotFoundError(f"The specified base directory does not exist: {BASE_DIR}")

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

app = Flask(__name__)

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

def get_entries(abs_path, req_path):
    entries = []
    for entry in os.listdir(abs_path):
        full_path = os.path.join(abs_path, entry)
        mod_time = os.path.getmtime(full_path)
        is_dir = os.path.isdir(full_path)
        is_image = entry.lower().endswith(IMAGE_EXTENSIONS)
        image_count = None
        if is_dir:
            image_count = sum(
                1 for item in os.listdir(full_path)
                if os.path.isfile(os.path.join(full_path, item)) and item.lower().endswith(IMAGE_EXTENSIONS)
            )

        entries.append({
            'name': entry,
            'path': os.path.join(req_path, entry).replace('\\', '/'),
            'is_dir': is_dir,
            'is_image': is_image,
            'mod_time': mod_time,
            'image_count': image_count
        })
    entries.sort(key=lambda x: x['mod_time'], reverse=True)
    return entries

def get_images(abs_path, req_path):
    images = []
    for entry in os.listdir(abs_path):
        full_path = os.path.join(abs_path, entry)
        if os.path.isfile(full_path) and entry.lower().endswith(IMAGE_EXTENSIONS):
            images.append({
                'name': entry,
                'path': os.path.join(req_path, entry).replace('\\', '/')
            })
    images.sort(key=lambda x: os.path.getmtime(os.path.join(abs_path, x['name'])), reverse=True)
    return images

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path):
        return "404 Not Found", 404

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    else:
        entries = get_entries(abs_path, req_path)
        return render_template('directory.html', entries=entries)

@app.route('/view/<path:req_path>')
def view_image(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)
    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        return "404 Not Found", 404
    if not abs_path.lower().endswith(IMAGE_EXTENSIONS):
        return "File not supported", 400

    dir_path = os.path.dirname(abs_path)
    dir_req_path = os.path.dirname(req_path)
    images = get_images(dir_path, dir_req_path)
    image_names = [img['name'] for img in images]
    current_image_name = os.path.basename(abs_path)
    if current_image_name in image_names:
        current_index = image_names.index(current_image_name)
    else:
        current_index = 0

    return render_template('image.html', images=images, current_index=current_index)

@app.route('/image/<path:filename>')
def serve_image(filename):
    safe_path = safe_join(BASE_DIR, filename)
    if not safe_path or not os.path.isfile(safe_path):
        return "404 Not Found", 404

    with open(safe_path, 'rb') as f:
        file_data = f.read()

    mime_type, _ = mimetypes.guess_type(safe_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    response = make_response(file_data)
    response.headers.set('Content-Type', mime_type)
    response.headers.set('Content-Length', len(file_data))
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8000)