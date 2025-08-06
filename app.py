from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import zipfile

app = Flask(__name__)

ROOT_FOLDER = 'images'
ZIP_OUTPUT_FOLDER = 'zips'

os.makedirs(ZIP_OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # List all zip files already generated
    zip_files = [f for f in os.listdir(ZIP_OUTPUT_FOLDER) if f.endswith('.zip')]
    return render_template('index.html', zip_files=zip_files)

@app.route('/zip_all_folders', methods=['POST'])
def zip_all_folders():
    entries = os.listdir(ROOT_FOLDER)

    for entry in entries:
        folder_path = os.path.join(ROOT_FOLDER, entry)
        if os.path.isdir(folder_path):
            zip_filename = f"{entry}.zip"
            zip_path = os.path.join(ZIP_OUTPUT_FOLDER, zip_filename)

            # Only create if it doesn't already exist
            if not os.path.exists(zip_path):
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            abs_file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_file_path, ROOT_FOLDER)
                            zf.write(abs_file_path, arcname=rel_path)

    return redirect(url_for('index'))

@app.route('/download_zip/<zipname>')
def download_zip(zipname):
    return send_from_directory(ZIP_OUTPUT_FOLDER, zipname, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
