from flask import Flask, render_template, request, send_file, jsonify, url_for
import pydicom
from pydicom.datadict import DicomDictionary
import io
import os
import zipfile
import tempfile

app = Flask(__name__, static_folder='static')

def get_dicom_headers():
    headers = []
    for tag, properties in DicomDictionary.items():
        name = properties[2]  # The name is the third item in the properties tuple
        header_id = f"({tag >> 16:04X},{tag & 0xFFFF:04X})"  # Format tag as (gggg,eeee)
        headers.append({"id": header_id, "name": name})
    return headers

def modify_dicom(file_path, modifications):
    ds = pydicom.dcmread(file_path)
    for mod in modifications:
        group, element, new_value = mod['group'], mod['element'], mod['value']
        tag = (int(group, 16), int(element, 16))
        
        if mod['cond_group'] and mod['cond_element'] and mod['cond_value']:
            cond_group, cond_element, cond_value = mod['cond_group'], mod['cond_element'], mod['cond_value']
            cond_tag = (int(cond_group, 16), int(cond_element, 16))
            
            if cond_tag in ds:
                if str(ds[cond_tag].value).strip() == cond_value.strip():
                    if tag in ds:
                        print(f'Making conditional edit: {tag}')
                        ds[tag].value = new_value
        else:
            if tag in ds:
                print(f'Making edit: {tag}')
                ds[tag].value = new_value
    
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
        cond_groups = request.form.getlist('cond_group[]')
        cond_elements = request.form.getlist('cond_element[]')
        cond_values = request.form.getlist('cond_value[]')

        modifications = []
        for i in range(len(groups)):
            mod = {
                'group': groups[i],
                'element': elements[i],
                'value': new_values[i],
                'cond_group': cond_groups[i] if i < len(cond_groups) else None,
                'cond_element': cond_elements[i] if i < len(cond_elements) else None,
                'cond_value': cond_values[i] if i < len(cond_values) else None
            }
            modifications.append(mod)

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
            with tempfile.NamedTemporaryFile(delete=False, suffix='.dcm') as temp_dcm:
                file.save(temp_dcm.name)
                modify_dicom(temp_dcm.name, modifications)
                return send_file(
                    temp_dcm.name,
                    as_attachment=True,
                    download_name="modified_dicom.dcm",
                    mimetype="application/dicom"
                )
    
    return render_template('index.html')

@app.route('/get_dicom_headers', methods=['GET'])
def dicom_headers():
    headers = get_dicom_headers()
    return jsonify(headers)

if __name__ == '__main__':
    app.run(debug=True)