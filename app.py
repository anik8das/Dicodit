from flask import Flask, render_template, request, send_file
import pydicom
import io

app = Flask(__name__)

def modify_dicom(file, header_code, new_value):
    # Read the DICOM file
    ds = pydicom.dcmread(file)
    
    # Modify the specified header
    ds[header_code].value = new_value
    
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
        
        # Get the header code and new value from the form
        header_code = request.form['header_code']
        new_value = request.form['new_value']
        
        # Modify the DICOM file
        modified_file = modify_dicom(file, header_code, new_value)
        
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