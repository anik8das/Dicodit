from flask import Flask, render_template, request, send_file
import pydicom
import io
import os

app = Flask(__name__)

def modify_dicom(file, group, element, new_value):
    # Read the DICOM file
    ds = pydicom.dcmread(file)
    
    # Convert group and element to integers
    group = int(group, 16)
    element = int(element, 16)
    
    # Modify the specified header
    ds[group, element].value = new_value
    
    # Save the modified DICOM to a BytesIO object
    modified_file = io.BytesIO()
    ds.save_as(modified_file)
    modified_file.seek(0)
    
    return modified_file

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['dicom_file']
        
        # Get the header code (group and element) and new value from the form
        group = request.form['header_group']
        element = request.form['header_element']
        new_value = request.form['new_value']
        
        # Modify the DICOM file
        modified_file = modify_dicom(file, group, element, new_value)
        
        # Send the modified file back to the user
        return send_file(
            modified_file,
            as_attachment=True,
            download_name="modified_dicom.dcm",
            mimetype="application/dicom"
        )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)