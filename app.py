from flask import Flask, render_template, request, send_file
import pydicom
import io
import os
import zipfile
import tempfile

app = Flask(__name__)

def modify_dicom(file_path, modifications):
    ds = pydicom.dcmread(file_path)
    for group, element, new_value in modifications:
        if (group, element) in ds:
            ds[group, element].value = new_value
    ds.save_as(file_path)

def process_zip(zip_path, modifications):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)
        
        for root, dirs, files in os.walk(tmpdirname):
            for filename in files:
                if filename.lower().endswith('.dcm'):
                    file_path = os.path.join(root, filename)
                    modify_dicom(file_path, modifications)
        
        output_zip = io.BytesIO()
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for root, dirs, files in os.walk(tmpdirname):
                for filename in files:
                    if filename.lower().endswith('.dcm'):
                        file_path = os.path.join(root, filename)
                        arcname = os.path.relpath(file_path, tmpdirname)
                        zipf.write(file_path, arcname)
        
        output_zip.seek(0)
        return output_zip

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['dicom_file']
        groups = request.form.getlist('header_group[]')
        elements = request.form.getlist('header_element[]')
        new_values = request.form.getlist('new_value[]')
        
        modifications = [
            (int(group, 16), int(element, 16), new_value)
            for group, element, new_value in zip(groups, elements, new_values)
        ]

        if file.filename.lower().endswith('.zip'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                file.save(temp_zip.name)
                output_zip = process_zip(temp_zip.name, modifications)
            os.unlink(temp_zip.name)
            return send_file(
                output_zip,
                as_attachment=True,
                download_name="modified_dicom_files.zip",
                mimetype="application/zip"
            )
        else:
            ds = pydicom.dcmread(file)
            for group, element, new_value in modifications:
                ds[group, element].value = new_value
            modified_file = io.BytesIO()
            ds.save_as(modified_file)
            modified_file.seek(0)
            return send_file(
                modified_file,
                as_attachment=True,
                download_name="modified_dicom.dcm",
                mimetype="application/dicom"
            )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)