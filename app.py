from flask import Flask, render_template, send_from_directory, send_file, safe_join, abort
import os
import io
import zipfile

app = Flask(__name__)

# Root directory to expose files/folders
ROOT_FOLDER = 'images'  # or rename to 'files' for clarity

@app.route('/')
def index():
    # List all files and folders (top-level only)
    entries = os.listdir(ROOT_FOLDER)
    files_and_folders = []
    for entry in entries:
        full_path = os.path.join(ROOT_FOLDER, entry)
        files_and_folders.append({
            'name': entry,
            'is_file': os.path.isfile(full_path),
            'is_folder': os.path.isdir(full_path)
        })
    return render_template('index.html', entries=files_and_folders)

@app.route('/download/<path:filename>')
def download_file(filename):
    filepath = safe_join(ROOT_FOLDER, filename)
    if not os.path.isfile(filepath):
        abort(404)
    return send_from_directory(ROOT_FOLDER, filename, as_attachment=True)

@app.route('/download_folder/<path:foldername>')
def download_folder(foldername):
    folderpath = safe_join(ROOT_FOLDER, foldername)
    if not os.path.isdir(folderpath):
        abort(404)

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folderpath):
            for file in files:
                abs_file_path = os.path.join(root, file)
                # Preserve relative folder structure in zip
                rel_path = os.path.relpath(abs_file_path, ROOT_FOLDER)
                zf.write(abs_file_path, arcname=rel_path)
    memory_file.seek(0)
    return send_file(memory_file,
                     download_name=f"{foldername}.zip",
                     as_attachment=True)

@app.route('/download_all')
def download_all():
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ROOT_FOLDER):
            for file in files:
                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, ROOT_FOLDER)
                zf.write(abs_file_path, arcname=rel_path)
    memory_file.seek(0)
    return send_file(memory_file,
                     download_name='all_content.zip',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
