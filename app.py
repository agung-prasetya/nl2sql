from flask import Flask, request, jsonify
from detectors import DMLDetector
import tempfile
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/dml/predict', methods=['POST'])
def predict():
    kalimat = request.form.get('kalimat')
    file = request.files.get('file')

    if not kalimat or not file:
        return jsonify({'error': 'Missing "kalimat" or file in request'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        detector = DMLDetector()
        predicted_label = detector.detect(kalimat=kalimat, file_database_json=tmp_path)
    finally:
        os.remove(tmp_path)

    return jsonify({
        'kalimat': kalimat,
        'predicted_label': predicted_label
    })

if __name__ == '__main__':
    app.run(debug=True)
