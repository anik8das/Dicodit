# Dicodit
Dicodit is the world's first online DICOM header editing tool. It allows users to quickly and easily modify DICOM headers directly in their web browser.

## Features
- Upload DICOM files
- Edit DICOM header tags
- Simple and intuitive user interface
- Instant processing and download of modified DICOM files

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- pip (Python package manager)

## Installation
1. Clone the repository: <br>
```git clone https://github.com/yourusername/dicodit.git``` <br>
```cd DICODIT```
2. Create a virtual environment (optional but recommended): <br>
```python -m venv venv``` <br>
```source venv/bin/activate  # On Windows use venv\Scripts\activate```
3. Install the required packages: <br>
```pip install Flask pydicom```

## Starting the Application
1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).
2. Run the Flask application: <br>
```python app.py```
3. Open a web browser and navigate to `http://127.0.0.1:5000/`

## Usage
1. Upload a DICOM file using the file picker.
2. Enter the DICOM tag you want to modify (Group and Element).
3. Enter the new value for the tag.
4. Check the conditional edit box if this edit only needs to applied to specific files
5. Click "Modify DICOM" to process and download the file.

## Contributing
Contributions to Dicodit are welcome. Please feel free to submit a Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
If you have any questions or feedback, please contact the project maintainers.

Thank you for using Dicodit!
