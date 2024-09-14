# Dicodit

Dicodit is an advanced online DICOM header/metadata editing tool. It allows users to quickly and easily modify DICOM headers directly in their web browser, supporting both individual DICOM files and batch processing with ZIP files.

## Features

- Upload individual DICOM files or ZIP archives containing multiple DICOM files
- Edit DICOM header tags with an intuitive search interface
- Perform conditional edits based on specific tag values
- Support for batch processing of multiple files
- Simple and user-friendly interface
- Instant processing and download of modified DICOM files or ZIP archives
- Responsive design for use on various devices

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dicodit.git
   cd dicodit
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install Flask pydicom
   ```

## Starting the Application

1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open a web browser and navigate to `http://127.0.0.1:5000/`

## Usage

1. Upload a DICOM file or ZIP archive using the file picker.
2. Use the search bar to find the DICOM tag you want to modify.
3. Enter the new value for the tag.
4. (Optional) Enable conditional editing by checking the box and specifying the condition.
5. Add more modifications as needed using the "Add Modification" button.
6. Click "Modify DICOM" to process and download the modified file(s).

## Contributing

Contributions to Dicodit are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

If you find Dicodit useful, consider supporting its development through the donation links provided in the application.

## Contact

If you have any questions or feedback, please don't hesitate to contact me at aniketdas001@gmail.com

Thank you for using Dicodit!
