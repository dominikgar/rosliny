from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)  # Pozwala na żądania cross-origin (przydatne podczas testowania lokalnego)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image' in data:
        image_data = data['image'].split(',')[1]  # Usuń przedrostek data:image/png;base64,
        try:
            image_bytes = base64.b64decode(image_data)
            filename = os.path.join(UPLOAD_FOLDER, 'captured_image.png')
            with open(filename, 'wb') as f:
                f.write(image_bytes)
            return jsonify({'message': 'Zdjęcie zostało odebrane przez serwer.'})
        except Exception as e:
            return jsonify({'error': f'Błąd dekodowania lub zapisu obrazu: {str(e)}'}), 400
    else:
        return jsonify({'error': 'Brak danych obrazu w żądaniu.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
