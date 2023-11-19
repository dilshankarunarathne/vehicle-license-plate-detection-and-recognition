from flask import Flask, render_template, request

from db import query_plate, add_info
from ocr import identify_plate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})


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
        print(results)

        return {'plate': plate, 'results': results}
        # return render_template('result.html', plate=plate, results=results)

    # return render_template('upload.html', error=True)
    return {'error': 'no file uploaded'}


@app.route('/add', methods=['POST'])
def add_details():
    data = request.get_json()
    plate = data['plate']
    name = data['name']
    phone = data['phone']
    address = data['address']

    try:
        add_info(plate, name, phone, address)
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True)
