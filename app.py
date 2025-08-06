from flask import Flask, render_template, send_from_directory, send_file
import os
import io
import zipfile

app = Flask(__name__)

# Folder where your images are stored
IMAGE_FOLDER = 'images'

@app.route('/')
def index():
    image_files = [f for f in os.listdir(IMAGE_FOLDER)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    return render_template('index.html', images=image_files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename, as_attachment=True)

@app.route('/download_all')
def download_all():
    # Create a zip in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for filename in os.listdir(IMAGE_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                zf.write(os.path.join(IMAGE_FOLDER, filename), arcname=filename)
    memory_file.seek(0)
    return send_file(memory_file,
                     download_name='all_images.zip',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
