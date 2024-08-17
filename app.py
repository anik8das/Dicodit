from flask import Flask, render_template, request, send_file
import pydicom
import io
import os
import zipfile
import tempfile

app = Flask(__name__)

def modify_dicom(file_path, group, element, new_value):
    ds = pydicom.dcmread(file_path)
    if (group, element) in ds:
        ds[group, element].value = new_value
    ds.save_as(file_path)

def process_zip(zip_path, group, element, new_value):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)
        
        # Process all DICOM files in the extracted directory, including nested folders
        for root, dirs, files in os.walk(tmpdirname):
            for filename in files:
                if filename.lower().endswith('.dcm'):
                    file_path = os.path.join(root, filename)
                    modify_dicom(file_path, group, element, new_value)
        
        # Create a new ZIP file with modified DICOM files
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
        group = int(request.form['header_group'], 16)
        element = int(request.form['header_element'], 16)
        new_value = request.form['new_value']

        if file.filename.lower().endswith('.zip'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                file.save(temp_zip.name)
                output_zip = process_zip(temp_zip.name, group, element, new_value)
            os.unlink(temp_zip.name)  # Delete the temporary file
            return send_file(
                output_zip,
                as_attachment=True,
                download_name="modified_dicom_files.zip",
                mimetype="application/zip"
            )
        else:
            # Single DICOM file processing
            ds = pydicom.dcmread(file)
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