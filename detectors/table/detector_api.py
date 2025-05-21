from detector import *
from flask import Flask, request, jsonify
import tempfile
import os
from flask_cors import CORS
from pathlib import Path


app = Flask(__name__)
CORS(app)

@app.route('/table/detect', methods=['POST'])
def predict_table():
    kalimat = request.form.get('kalimat')
    file = request.files.get('file')

    if not kalimat or not file:
        return jsonify({'error': 'Missing "kalimat" or "file database json" in request'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        detector = TableDetector()
        detected_label = detector.detect(kalimat=kalimat,filepath_database_json=tmp_path)
    finally:
        os.remove(tmp_path)

    return jsonify({
        'kalimat': kalimat,
        'detected_label': detected_label
    })


if __name__ == '__main__':
    app.run(debug=True)