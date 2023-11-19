from flask import Flask, render_template, request

from db import query_plate
from ocr import identify_plate

app = Flask(__name__)


@app.route('/')
def upload_page():
    return render_template('upload.html')


@app.route('/process', methods=['POST'])
def process_image():
    # Get the uploaded image
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Save the uploaded image
        uploaded_file.save('uploaded_image.jpg')

        plate = identify_plate('uploaded_image.jpg')

        results = query_plate(plate)

        return render_template('result.html', plate=plate)

    return render_template('upload.html', error=True)


if __name__ == '__main__':
    app.run(debug=True)
